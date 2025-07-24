#pragma once

#include "windows.h"
#include "DisplayInterface.h"
#include <string.h>
#include <string>
#include <string>
#include <comdef.h>
#define INTEL_VENDOR_ID 0x8086
#define CTL_DLL_PATH "C:\\Windows\\System32\\ControlLib.dll"
#define CTL_LIB "ControlLib.dll"

char LIBRARY_NAME[22] = "ControlAPI.dll";

// Convert RGB to YUV
static double RGB2YCbCr709[3][3] = { { 0.2126, 0.7152, 0.0722 }, { -0.1146, -0.3854, 0.5000 }, { 0.5000, -0.4542, -0.0458 } };

// Convert YUV to RGB
static double YCbCr2RGB709[3][3] = { { 1.0000, 0.0000, 1.5748 }, { 1.0000, -0.1873, -0.4681 }, { 1.0000, 1.8556, 0.0000 } };

CTRL_API_CONTEXT         apiContext = { NULL };
ctl_mux_output_handle_t *handle;

bool ControlAPIInitialize(ctl_init_args_t *argsInit)
{
    ctl_init_args_t initArgs;
    HINSTANCE       libraryHandle = NULL;

    initArgs.AppVersion = argsInit->AppVersion;
    initArgs.flags      = 0;
    initArgs.Size       = sizeof(initArgs);
    initArgs.Version    = 0;

    initArgs.ApplicationUID = argsInit->ApplicationUID; // Default IGCC GUID

    ZeroMemory(&apiContext, sizeof(CTRL_API_CONTEXT));
    libraryHandle = LoadLibrary(TEXT(CTL_DLL_PATH));
    if (libraryHandle == NULL)
    {
        libraryHandle = LoadLibrary(TEXT(CTL_LIB));
        DEBUG_LOG("Control API DLL loaded from Bin folder");
    }

    DEBUG_LOG("Control API DLL loaded from System32 folder");
    NULL_PTR_CHECK(libraryHandle);
    apiContext.pfnCtrlApiInitialize                  = (ctl_pfnInit_t)GetProcAddress(libraryHandle, "ctlInit");
    apiContext.pfnCtrlApiCleanup                     = (ctl_pfnClose_t)GetProcAddress(libraryHandle, "ctlClose");
    apiContext.pfnEnumerateDevices                   = (ctl_pfnEnumerateDevices_t)GetProcAddress(libraryHandle, "ctlEnumerateDevices");
    apiContext.pfnEnumerateMuxDevices                = (ctl_pfnEnumerateMuxDevices_t)GetProcAddress(libraryHandle, "ctlEnumerateMuxDevices");
    apiContext.pfnGetMuxProperties                   = (ctl_pfnGetMuxProperties_t)GetProcAddress(libraryHandle, "ctlGetMuxProperties");
    apiContext.pfnSwitchMux                          = (ctl_pfnSwitchMux_t)GetProcAddress(libraryHandle, "ctlSwitchMux");
    apiContext.pfnGetDeviceProperties                = (ctl_pfnGetDeviceProperties_t)GetProcAddress(libraryHandle, "ctlGetDeviceProperties");
    apiContext.pfnEnumerateDisplayOutputs            = (ctl_pfnEnumerateDisplayOutputs_t)GetProcAddress(libraryHandle, "ctlEnumerateDisplayOutputs");
    apiContext.pfnGetDisplayProperties               = (ctl_pfnGetDisplayProperties_t)GetProcAddress(libraryHandle, "ctlGetDisplayProperties");
    apiContext.pfnGetDisplayEncoderProperties        = (ctl_pfnGetAdaperDisplayEncoderProperties_t)GetProcAddress(libraryHandle, "ctlGetAdaperDisplayEncoderProperties");
    apiContext.pfnCheckDriverVersion                 = (ctl_pfnCheckDriverVersion_t)GetProcAddress(libraryHandle, "ctlCheckDriverVersion");
    apiContext.pfnGetZeDevice                        = (ctl_pfnGetZeDevice_t)GetProcAddress(libraryHandle, "ctlGetZeDevice");
    apiContext.pfnI2CAccess                          = (ctl_pfnI2CAccess_t)GetProcAddress(libraryHandle, "ctlI2CAccess");
    apiContext.pfnAUXAccess                          = (ctl_pfnAUXAccess_t)GetProcAddress(libraryHandle, "ctlAUXAccess");
    apiContext.pfnGetSharpnessCaps                   = (ctl_pfnGetSharpnessCaps_t)GetProcAddress(libraryHandle, "ctlGetSharpnessCaps");
    apiContext.pfnGetCurrentSharpness                = (ctl_pfnGetCurrentSharpness_t)GetProcAddress(libraryHandle, "ctlGetCurrentSharpness");
    apiContext.pfnSetCurrentSharpness                = (ctl_pfnSetCurrentSharpness_t)GetProcAddress(libraryHandle, "ctlSetCurrentSharpness");
    apiContext.pfnPanelDescriptorAccess              = (ctl_pfnPanelDescriptorAccess_t)GetProcAddress(libraryHandle, "ctlPanelDescriptorAccess");
    apiContext.pfnPixelTransformationGetConfig       = (ctl_pfnPixelTransformationGetConfig_t)GetProcAddress(libraryHandle, "ctlPixelTransformationGetConfig");
    apiContext.pfnPixelTransformationSetConfig       = (ctl_pfnPixelTransformationSetConfig_t)GetProcAddress(libraryHandle, "ctlPixelTransformationSetConfig");
    apiContext.pfnGetPowerOptimizationCaps           = (ctl_pfnGetPowerOptimizationCaps_t)GetProcAddress(libraryHandle, "ctlGetPowerOptimizationCaps");
    apiContext.pfnGetPowerOptimizationSetting        = (ctl_pfnGetPowerOptimizationSetting_t)GetProcAddress(libraryHandle, "ctlGetPowerOptimizationSetting");
    apiContext.pfnSetPowerOptimizationSetting        = (ctl_pfnSetPowerOptimizationSetting_t)GetProcAddress(libraryHandle, "ctlSetPowerOptimizationSetting");
    apiContext.pfnGetSupportedRetroScalingCapability = (ctl_pfnGetSupportedRetroScalingCapability_t)GetProcAddress(libraryHandle, "ctlGetSupportedRetroScalingCapability");
    apiContext.pfnGetSetRetroScaling                 = (ctl_pfnGetSetRetroScaling_t)GetProcAddress(libraryHandle, "ctlGetSetRetroScaling");
    apiContext.pfnGetSupportedScalingCapability      = (ctl_pfnGetSupportedScalingCapability_t)GetProcAddress(libraryHandle, "ctlGetSupportedScalingCapability");
    apiContext.pfnGetCurrentScaling                  = (ctl_pfnGetCurrentScaling_t)GetProcAddress(libraryHandle, "ctlGetCurrentScaling");
    apiContext.pfnSetCurrentScaling                  = (ctl_pfnSetCurrentScaling_t)GetProcAddress(libraryHandle, "ctlSetCurrentScaling");
    apiContext.pfnGetSet3DFeature                    = (ctl_pfnGetSet3DFeature_t)GetProcAddress(libraryHandle, "ctlGetSet3DFeature");
    apiContext.pfnGetLACEConfig                      = (ctl_pfnGetLACEConfig_t)GetProcAddress(libraryHandle, "ctlGetLACEConfig");
    apiContext.pfnSetLACEConfig                      = (ctl_pfnSetLACEConfig_t)GetProcAddress(libraryHandle, "ctlSetLACEConfig");
    apiContext.pfnGetIntelArcSyncInfoForMonitor      = (ctl_pfnGetIntelArcSyncInfoForMonitor_t)GetProcAddress(libraryHandle, "ctlGetIntelArcSyncInfoForMonitor");
    apiContext.pfnGetIntelArcSyncProfile             = (ctl_pfnGetIntelArcSyncProfile_t)GetProcAddress(libraryHandle, "ctlGetIntelArcSyncProfile");
    apiContext.pfnSetIntelArcSyncProfile             = (ctl_pfnSetIntelArcSyncProfile_t)GetProcAddress(libraryHandle, "ctlSetIntelArcSyncProfile");
    apiContext.pfnSetBrightnessSetting               = (ctl_pfnSetBrightnessSetting_t)GetProcAddress(libraryHandle, "ctlSetBrightnessSetting");
    apiContext.pfnGetBrightnessSetting               = (ctl_pfnGetBrightnessSetting_t)GetProcAddress(libraryHandle, "ctlGetBrightnessSetting");
    apiContext.pfnEdidManagement                     = (ctl_pfnEdidManagement_t)GetProcAddress(libraryHandle, "ctlEdidManagement");
    apiContext.pfnGetSetDisplayGenlock               = (ctl_pfnGetSetDisplayGenlock_t)GetProcAddress(libraryHandle, "ctlGetSetDisplayGenlock");
    apiContext.pfnGetSetWireFormat                   = (ctl_pfnGetSetWireFormat_t)GetProcAddress(libraryHandle, "ctlGetSetWireFormat");
    apiContext.pfnGetSetCombinedDisplay              = (ctl_pfnGetSetCombinedDisplay_t)GetProcAddress(libraryHandle, "ctlGetSetCombinedDisplay");
    NULL_PTR_CHECK(apiContext.pfnCtrlApiInitialize);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnCtrlApiInitialize(&initArgs, &apiContext.apiHandle));
    DEBUG_LOG("Control API Supported Version %d, App Version %d", initArgs.SupportedVersion, initArgs.AppVersion);
    return TRUE;
}

bool ControlAPICleanup()
{
    NULL_PTR_CHECK(apiContext.pfnCtrlApiCleanup);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnCtrlApiCleanup(apiContext.apiHandle));
    return TRUE;
}

bool ControlApiEnumerateDevices(ctl_api_handle_t hAPIHandle, uint32_t *pCount, ctl_device_adapter_handle_t *phDevices)
{
    NULL_PTR_CHECK(apiContext.pfnEnumerateDevices);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnEnumerateDevices(hAPIHandle, pCount, phDevices));
    return TRUE;
}

bool ControlApiEnumerateMuxDevices(ctl_api_handle_t hAPIHandle, uint32_t *pCount, ctl_mux_output_handle_t *phMuxDevices)
{
    NULL_PTR_CHECK(apiContext.pfnEnumerateMuxDevices);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnEnumerateMuxDevices(hAPIHandle, pCount, phMuxDevices));
    return TRUE;
}

bool ControlApiEnumerateDisplayOutputs(ctl_device_adapter_handle_t hDeviceAdapter, uint32_t *pCount, ctl_display_output_handle_t *phDisplayOutputs)
{
    NULL_PTR_CHECK(apiContext.pfnEnumerateDisplayOutputs);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnEnumerateDisplayOutputs(hDeviceAdapter, pCount, phDisplayOutputs));
    return TRUE;
}

bool ControlApiGetDisplayProperties(ctl_display_output_handle_t hDisplayOutput, ctl_display_properties_t *pProperties)
{
    NULL_PTR_CHECK(apiContext.pfnGetDisplayProperties);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetDisplayProperties(hDisplayOutput, pProperties));
    return TRUE;
}

bool ControlApiGetMuxProperties(ctl_mux_output_handle_t hMuxDevice, ctl_mux_properties_t *pMuxProperties)
{
    NULL_PTR_CHECK(apiContext.pfnGetMuxProperties);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetMuxProperties(hMuxDevice, pMuxProperties));
    return TRUE;
}

bool ControlApiSwitchMux(ctl_mux_output_handle_t hMuxDevice, ctl_display_output_handle_t hInactiveDisplayOutput)
{
    NULL_PTR_CHECK(apiContext.pfnSwitchMux);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSwitchMux(hMuxDevice, hInactiveDisplayOutput));
    return TRUE;
}

bool ControlApiGetDisplayEncoderProperties(ctl_display_output_handle_t hDisplayOutput, ctl_adapter_display_encoder_properties_t *pProperties)
{
    NULL_PTR_CHECK(apiContext.pfnGetDisplayEncoderProperties);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetDisplayEncoderProperties(hDisplayOutput, pProperties));
    return TRUE;
}

bool ControlApiGetDeviceProperties(ctl_device_adapter_handle_t hDAhandle, ctl_device_adapter_properties_t *pProperties)
{
    NULL_PTR_CHECK(pProperties);
    NULL_PTR_CHECK(apiContext.pfnGetDeviceProperties);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetDeviceProperties(hDAhandle, pProperties));
    return TRUE;
}

bool ControlApiCheckDriverVersion(ctl_device_adapter_handle_t hDeviceAdapter, ctl_version_info_t version_info)
{
    NULL_PTR_CHECK(apiContext.pfnCheckDriverVersion);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnCheckDriverVersion(hDeviceAdapter, version_info));
    return TRUE;
}

bool ControlApiGetZeDevice(ctl_device_adapter_handle_t hDAhandle, void *pZeDevice, void **hInstance)
{
    NULL_PTR_CHECK(apiContext.pfnGetZeDevice);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetZeDevice(hDAhandle, pZeDevice, hInstance));
    return TRUE;
}

bool ControlApiI2cAccess(ctl_display_output_handle_t hDisplayOutput, ctl_i2c_access_args_t *pI2CAccessArgs)
{
    NULL_PTR_CHECK(apiContext.pfnI2CAccess);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnI2CAccess(hDisplayOutput, pI2CAccessArgs));
    return TRUE;
}

bool ControlApiAuxAccess(ctl_display_output_handle_t hDisplayOutput, ctl_aux_access_args_t *pAuxAccessArgs)
{
    NULL_PTR_CHECK(apiContext.pfnAUXAccess);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnAUXAccess(hDisplayOutput, pAuxAccessArgs));
    return TRUE;
}

bool ControlApiGetSharpnessCaps(ctl_display_output_handle_t hDisplayOutput, ctl_sharpness_caps_t *pSharpnessCaps)
{
    NULL_PTR_CHECK(apiContext.pfnGetSharpnessCaps);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSharpnessCaps(hDisplayOutput, pSharpnessCaps));
    return TRUE;
}

bool ControlApiGetCurrentSharpness(ctl_display_output_handle_t hDisplayOutput, ctl_sharpness_settings_t *pSharpnessSettings)
{
    NULL_PTR_CHECK(apiContext.pfnGetCurrentSharpness);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetCurrentSharpness(hDisplayOutput, pSharpnessSettings));
    return TRUE;
}

bool ControlApiSetCurrentSharpness(ctl_display_output_handle_t hDisplayOutput, ctl_sharpness_settings_t *pSharpnessSettings)
{
    NULL_PTR_CHECK(apiContext.pfnSetCurrentSharpness);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetCurrentSharpness(hDisplayOutput, pSharpnessSettings));
    return TRUE;
}

bool ControlApiPanelDescriptorAccess(ctl_display_output_handle_t hDisplayOutput, ctl_panel_descriptor_access_args_t *pPanelDescriptorAccessArgs)
{
    NULL_PTR_CHECK(apiContext.pfnPanelDescriptorAccess);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnPanelDescriptorAccess(hDisplayOutput, pPanelDescriptorAccessArgs));
    return TRUE;
}

bool ControlApiPixelTransformationGetConfig(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pPixTxGetConfigArgs)
{
    NULL_PTR_CHECK(apiContext.pfnPixelTransformationGetConfig);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnPixelTransformationGetConfig(hDisplayOutput, pPixTxGetConfigArgs));
    return TRUE;
}

bool ControlApiPixelTransformationSetConfig(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_set_config_t *pPixTxSetConfigArgs)
{
    NULL_PTR_CHECK(apiContext.pfnPixelTransformationSetConfig);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnPixelTransformationSetConfig(hDisplayOutput, pPixTxSetConfigArgs));
    return TRUE;
}

bool ControlApiGetPowerOptimizationCaps(ctl_display_output_handle_t hDisplayOutput, ctl_power_optimization_caps_t *pPowerOptimizationCaps)
{
    NULL_PTR_CHECK(apiContext.pfnGetPowerOptimizationCaps);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetPowerOptimizationCaps(hDisplayOutput, pPowerOptimizationCaps));
    return TRUE;
}

bool ControlApiGetPowerOptimizationSetting(ctl_display_output_handle_t hDisplayOutput, ctl_power_optimization_settings_t *pPowerOptimizationSettings)
{
    NULL_PTR_CHECK(apiContext.pfnGetPowerOptimizationSetting);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetPowerOptimizationSetting(hDisplayOutput, pPowerOptimizationSettings));
    return TRUE;
}

bool ControlApiSetPowerOptimizationSetting(ctl_display_output_handle_t hDisplayOutput, ctl_power_optimization_settings_t *pPowerOptimizationSettings)
{
    NULL_PTR_CHECK(apiContext.pfnSetPowerOptimizationSetting);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetPowerOptimizationSetting(hDisplayOutput, pPowerOptimizationSettings));
    return TRUE;
}

bool ControlApiGetSetRetroScaling(ctl_device_adapter_handle_t hDAhandle, ctl_retro_scaling_settings_t *pGetSetRetroScalingType)
{
    NULL_PTR_CHECK(apiContext.pfnGetSetRetroScaling);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSetRetroScaling(hDAhandle, pGetSetRetroScalingType));
    return TRUE;
}

bool ControlApiGetSupportedRetroScalingCapability(ctl_device_adapter_handle_t hDAhandle, ctl_retro_scaling_caps_t *pRetroScalingCaps)
{
    NULL_PTR_CHECK(apiContext.pfnGetSupportedRetroScalingCapability);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSupportedRetroScalingCapability(hDAhandle, pRetroScalingCaps));
    return TRUE;
}

bool ControlApiGetSupportedScalingCapability(ctl_display_output_handle_t hDisplayOutput, ctl_scaling_caps_t *pScalingCaps)
{
    NULL_PTR_CHECK(apiContext.pfnGetSupportedScalingCapability);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSupportedScalingCapability(hDisplayOutput, pScalingCaps));
    return TRUE;
}

bool ControlApiGetCurrentScaling(ctl_display_output_handle_t hDisplayOutput, ctl_scaling_settings_t *pSetScalingType)
{
    NULL_PTR_CHECK(apiContext.pfnGetCurrentScaling);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetCurrentScaling(hDisplayOutput, pSetScalingType));
    return TRUE;
}

bool ControlApiSetCurrentScaling(ctl_display_output_handle_t hDisplayOutput, ctl_scaling_settings_t *pSetScalingType)
{
    NULL_PTR_CHECK(apiContext.pfnSetCurrentScaling);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetCurrentScaling(hDisplayOutput, pSetScalingType));
    return TRUE;
}

bool ControlAPIGetSetWireFormat(ctl_display_output_handle_t hDisplayOutput, ctl_get_set_wire_format_config_t *pGetSetWireFormatSetting)
{
    INFO_LOG("ctlGetSetWireFormat");
    NULL_PTR_CHECK(apiContext.pfnGetSetWireFormat);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSetWireFormat(hDisplayOutput, pGetSetWireFormatSetting));
    return TRUE;
}

bool ControlApiGetSet3DFeature(ctl_device_adapter_handle_t hDAhandle, ctl_3d_feature_getset_t *pFeature)
{
    NULL_PTR_CHECK(apiContext.pfnGetSet3DFeature);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSet3DFeature(hDAhandle, pFeature));
    return TRUE;
}

bool ControlApiGetLaces(ctl_display_output_handle_t hDisplayOutput, ctl_lace_config_t *pGetLaceConfig)
{
    NULL_PTR_CHECK(apiContext.pfnGetLACEConfig);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetLACEConfig(hDisplayOutput, pGetLaceConfig));
    return TRUE;
}

bool ControlApiSetLaces(ctl_display_output_handle_t hDisplayOutput, ctl_lace_config_t *pSetLaceConfig)
{
    NULL_PTR_CHECK(apiContext.pfnSetLACEConfig);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetLACEConfig(hDisplayOutput, pSetLaceConfig));
    return TRUE;
}

bool ControlApiGetIntelArcSyncInfoForMonitor(ctl_display_output_handle_t hDisplayOutput, ctl_intel_arc_sync_monitor_params_t *pGetIntelArcSyncMonitorParams)
{
    NULL_PTR_CHECK(apiContext.pfnGetIntelArcSyncInfoForMonitor);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetIntelArcSyncInfoForMonitor(hDisplayOutput, pGetIntelArcSyncMonitorParams));
    return TRUE;
}

bool ControlApiSetIntelArcSyncProfile(ctl_display_output_handle_t hDisplayOutput, _ctl_intel_arc_sync_profile_params_t *pSetIntelArcSyncProfileParams)
{
    NULL_PTR_CHECK(apiContext.pfnSetIntelArcSyncProfile);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetIntelArcSyncProfile(hDisplayOutput, pSetIntelArcSyncProfileParams));
    return TRUE;
}

bool ControlApiGetIntelArcSyncProfile(ctl_display_output_handle_t hDisplayOutput, _ctl_intel_arc_sync_profile_params_t *pGetIntelArcSyncProfileParams)
{
    NULL_PTR_CHECK(apiContext.pfnGetIntelArcSyncProfile);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetIntelArcSyncProfile(hDisplayOutput, pGetIntelArcSyncProfileParams));
    return TRUE;
}

bool ControlApiSetBrightnessSettings(ctl_display_output_handle_t hDisplayOutput, ctl_set_brightness_t *pSetBrightnessSetting)
{
    NULL_PTR_CHECK(apiContext.pfnSetBrightnessSetting);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnSetBrightnessSetting(hDisplayOutput, pSetBrightnessSetting));
    return TRUE;
}

bool ControlApiGetBrightnessSettings(ctl_display_output_handle_t hDisplayOutput, ctl_get_brightness_t *pGetBrightnessSetting)
{
    NULL_PTR_CHECK(apiContext.pfnGetBrightnessSetting);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetBrightnessSetting(hDisplayOutput, pGetBrightnessSetting));
    return TRUE;
}

bool ControlAPIEDIDManagementEx(ctl_display_output_handle_t hDisplayOutput, ctl_edid_management_args_t *pEDIDManagementArgs)
{
    NULL_PTR_CHECK(apiContext.pfnEdidManagement);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnEdidManagement(hDisplayOutput, pEDIDManagementArgs));
    return TRUE;
}

bool ControlAPIGetSetDisplayGenlockEx(ctl_device_adapter_handle_t *hDeviceAdapter, ctl_genlock_args_t *pGenlockArgs, uint32_t AdapterCount,
                                      ctl_device_adapter_handle_t *hFailureDeviceAdapter)
{
    NULL_PTR_CHECK(apiContext.pfnGetSetDisplayGenlock);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSetDisplayGenlock(hDeviceAdapter, pGenlockArgs, AdapterCount, hFailureDeviceAdapter));
    return TRUE;
}

bool ControlAPIGetSetCombinedDisplayEx(ctl_device_adapter_handle_t hDevice, ctl_combined_display_args_t *pCombinedDisplayArgs)
{
    NULL_PTR_CHECK(apiContext.pfnGetSetCombinedDisplay);
    VERIFY_ONECORE_API_STATUS(apiContext.pfnGetSetCombinedDisplay(hDevice, pCombinedDisplayArgs));
    return TRUE;
}

bool GetActiveDisplay(uint32_t *pDisplayCount, ctl_display_output_handle_t *hDisplayOutput, ctl_display_output_handle_t *hDisplayActive, uint32_t targetID)
{
    bool                     apiResult         = TRUE;
    uint32_t                 index             = 0;
    uint32_t                 displayIndex      = 0;
    uint32_t                 count             = 0;
    ctl_display_properties_t displayProperties = { 0 };
    bool                     displayActive;
    bool                     displayAttached;
    uint32_t                 displayCount = *pDisplayCount;

    for (index = 0; index < displayCount; index++)
    {
        displayActive                                                       = FALSE;
        displayAttached                                                     = FALSE;
        displayProperties.Size                                              = sizeof(ctl_display_properties_t);
        displayProperties.DisplayConfigFlags                                = 0;
        displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID = 0;

        if (NULL != hDisplayOutput[index])
        {
            apiResult = ControlApiGetDisplayProperties(hDisplayOutput[index], &displayProperties);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API GetDisplayOutputProperties Failed");
            }
            else
            {
                displayActive   = displayProperties.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ACTIVE;
                displayAttached = displayProperties.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ATTACHED;
                if (displayActive && displayAttached && (targetID == displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID))
                {
                    hDisplayActive[displayIndex++] = hDisplayOutput[index];
                    count                          = count + 1;
                }
            }
        }
    }
    *pDisplayCount = count;
    return apiResult;
}

bool GetDisplayHandle(uint32_t *pDisplayCount, ctl_display_output_handle_t *hDisplayOutput, ctl_display_output_handle_t *hDisplayTest, uint32_t targetID)
{
    bool                     apiResult         = TRUE;
    uint32_t                 index             = 0;
    uint32_t                 displayIndex      = 0;
    uint32_t                 count             = 0;
    ctl_display_properties_t displayProperties = { 0 };
    bool                     displayActive;
    bool                     displayAttached;
    uint32_t                 displayCount = *pDisplayCount;

    for (index = 0; index < displayCount; index++)
    {
        displayActive                                                       = FALSE;
        displayAttached                                                     = FALSE;
        displayProperties.Size                                              = sizeof(ctl_display_properties_t);
        displayProperties.DisplayConfigFlags                                = 0;
        displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID = 0;

        if (NULL != hDisplayOutput[index])
        {
            apiResult = ControlApiGetDisplayProperties(hDisplayOutput[index], &displayProperties);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API GetDisplayOutputProperties Failed");
            }
            else
            {
                if (targetID == displayProperties.Os_display_encoder_handle.WindowsDisplayEncoderID)
                {
                    hDisplayTest[displayIndex++] = hDisplayOutput[index];
                    ++count;
                }
            }
        }
    }
    *pDisplayCount = count;
    return apiResult;
}

bool GetActiveAdapter(uint32_t *pDeviceCount, ctl_device_adapter_handle_t *hDevice, ctl_device_adapter_handle_t *hDeviceAdapter, WCHAR *deviceID)
{
    bool                            apiResult               = TRUE;
    uint32_t                        deviceIndex             = 0;
    uint32_t                        adapterIndex            = 0;
    uint32_t                        count                   = 0;
    ctl_device_adapter_properties_t deviceAdapterProperties = { 0 };
    uint32_t                        deviceCount             = *pDeviceCount;
    LUID                            adapterID;
    char                            ctlDeviceID[33];

    for (deviceIndex = 0; deviceIndex < deviceCount; deviceIndex++)
    {
        if (NULL != hDevice[deviceIndex])
        {
            deviceAdapterProperties.Size      = sizeof(ctl_device_adapter_properties_t);
            deviceAdapterProperties.pDeviceID = malloc(sizeof(LUID));
            NULL_PTR_CHECK(deviceAdapterProperties.pDeviceID);
            deviceAdapterProperties.device_id_size = sizeof(LUID);

            VERIFY_API_STATUS(ControlApiGetDeviceProperties(hDevice[deviceIndex], &deviceAdapterProperties));
            if (CTL_DEVICE_TYPE_GRAPHICS != deviceAdapterProperties.device_type)
            {
                DEBUG_LOG("This is not a Graphics Device \n");
                FREE_MEMORY(deviceAdapterProperties.pDeviceID);
                continue;
            }

            adapterID = *(reinterpret_cast<LUID *>(deviceAdapterProperties.pDeviceID));

            sprintf(ctlDeviceID, "%X", deviceAdapterProperties.pci_device_id);
            const char *deviceIDUpdated = static_cast<const char *>(_bstr_t(deviceID));

            if ((INTEL_VENDOR_ID == deviceAdapterProperties.pci_vendor_id) && (strcmp(ctlDeviceID, deviceIDUpdated) == 0))
            {
                hDeviceAdapter[adapterIndex++] = hDevice[deviceIndex];
                count                          = count + 1;
            }
        }
    }

    *pDeviceCount = count;
    FREE_MEMORY(deviceAdapterProperties.pDeviceID);
    return apiResult;
}

bool ControlAPIGetDisplayProperties(ctl_display_properties_t *displayProperties, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult             = TRUE;
    uint32_t                     displayIndex          = 0;
    uint32_t                     adapterIndex          = 0;
    uint32_t                     displayCount          = 0;
    uint32_t                     adapterCount          = 0;
    ctl_device_adapter_handle_t *hDevices              = nullptr;
    ctl_device_adapter_handle_t *hActDevices           = nullptr;
    ctl_display_output_handle_t *hDisplayOutput        = nullptr;
    ctl_display_output_handle_t *hDisplayActive        = nullptr;
    ctl_display_properties_t     displayPropertiesArgs = { 0 };
    bool                         displayActive;
    bool                         displayAttached;
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetDisplayProperties !!!");
        goto END;
    }
    DEBUG_LOG("ControlApiGetDisplayProperties adapterCount %d ", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        displayCount = 0;
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);

        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPIGetDisplayProperties Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlApiGetDisplayProperties displayCount %d ", displayCount);

        displayActive                                                           = FALSE;
        displayAttached                                                         = FALSE;
        displayPropertiesArgs.Size                                              = sizeof(ctl_display_properties_t);
        displayPropertiesArgs.DisplayConfigFlags                                = 0;
        displayPropertiesArgs.Os_display_encoder_handle.WindowsDisplayEncoderID = 0;

        if (NULL != hDisplayActive[displayIndex])
        {
            apiResult       = ControlApiGetDisplayProperties(hDisplayActive[displayIndex], &displayPropertiesArgs);
            displayActive   = displayPropertiesArgs.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ACTIVE;
            displayAttached = displayPropertiesArgs.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ATTACHED;
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API GetDisplayOutputProperties Failed");
                goto END;
            }
            else
            {
                INFO_LOG("Display TargetID %d", displayPropertiesArgs.Os_display_encoder_handle.WindowsDisplayEncoderID);
                INFO_LOG("Display Active %d", displayActive);
                INFO_LOG("Display Attached %d", displayAttached);
                DEBUG_LOG("AttachedDisplayMuxType %d", displayPropertiesArgs.AttachedDisplayMuxType);
                DEBUG_LOG("DisplayConfigFlags %d", displayPropertiesArgs.DisplayConfigFlags);
                DEBUG_LOG("AdvancedFeatureEnabledFlags %d", displayPropertiesArgs.AdvancedFeatureEnabledFlags);
                DEBUG_LOG("ProtocolConverterOutput %d", displayPropertiesArgs.ProtocolConverterOutput);
                DEBUG_LOG("AdvancedFeatureSupportedFlags %d", displayPropertiesArgs.AdvancedFeatureSupportedFlags);
                DEBUG_LOG("SupportedSpec - Major %d, Minor %d, Revision %d", displayPropertiesArgs.SupportedSpec.major_version, displayPropertiesArgs.SupportedSpec.minor_version,
                          displayPropertiesArgs.SupportedSpec.revision_version);
                DEBUG_LOG("SupportedOutputBPCFlags %d", displayPropertiesArgs.SupportedOutputBPCFlags);
                DEBUG_LOG("Display_Timing_Info - HActive:%d, VActive:%d, HActive:%d, RefreshRate:%d, PixelClock:%d, VSync:%d, VTotal:%d, HTotal:%d,",
                          displayPropertiesArgs.Display_Timing_Info.HActive, displayPropertiesArgs.Display_Timing_Info.VActive,
                          displayPropertiesArgs.Display_Timing_Info.RefreshRate, displayPropertiesArgs.Display_Timing_Info.PixelClock,
                          displayPropertiesArgs.Display_Timing_Info.VSync, displayPropertiesArgs.Display_Timing_Info.VTotal, displayPropertiesArgs.Display_Timing_Info.HTotal);
                DEBUG_LOG("FeatureEnabledFlags %d", displayPropertiesArgs.FeatureEnabledFlags);
                DEBUG_LOG("FeatureSupportedFlags %d", displayPropertiesArgs.FeatureSupportedFlags);
                memcpy(displayProperties, &displayPropertiesArgs, sizeof(ctl_display_properties_t));
            }
        }
    }
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    return apiResult;
}

bool ControlAPISwitchMux()
{
    bool                            apiResult                    = TRUE;
    ctl_device_adapter_properties_t StDeviceAdapterProperties[2] = { 0 };
    ctl_mux_properties_t            MuxProperties                = { 0 };
    uint32_t                        DisplayCount[2]              = { 0 };
    ctl_display_output_handle_t *   hDisplayOutput[2]            = { 0 };
    ctl_display_output_handle_t     ActiveDisplayOut             = { 0 };
    ctl_display_output_handle_t     InActiveDisplayOutput        = { 0 };
    uint32_t                        AdapterCount                 = 0;
    uint32_t                        DispCount                    = 0;
    uint32_t                        Index                        = 0;
    uint32_t                        MuxCount                     = 0;
    ctl_device_adapter_handle_t *   hDevices                     = nullptr;
    ctl_mux_output_handle_t *       hMuxDevices                  = nullptr;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &AdapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * AdapterCount);
    NULL_PTR_CHECK(hDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &AdapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        FREE_MEMORY(hDevices);
        return apiResult;
    }
    INFO_LOG("ControlApiGetDisplayProperties adapterCount %d ", AdapterCount);
    if (AdapterCount != 2)
    {
        ERROR_LOG("Unsupported feature with more/less than 2 Adapters!!!");
        return apiResult;
    }

    for (Index = 0; Index < AdapterCount; Index++)
    {
        StDeviceAdapterProperties[Index].Size           = sizeof(ctl_device_adapter_properties_t);
        StDeviceAdapterProperties[Index].pDeviceID      = malloc(sizeof(LUID));
        StDeviceAdapterProperties[Index].device_id_size = sizeof(LUID);

        VERIFY_API_STATUS(ControlApiGetDeviceProperties(hDevices[Index], &StDeviceAdapterProperties[Index]));
        if (CTL_DEVICE_TYPE_GRAPHICS != StDeviceAdapterProperties[Index].device_type)
        {
            DEBUG_LOG("This is not a Graphics Device \n");
            FREE_MEMORY(StDeviceAdapterProperties[Index].pDeviceID);
            continue;
        }

        DEBUG_LOG("Graphics adapter: %d", StDeviceAdapterProperties[Index].graphics_adapter_properties);

        // Enumerate all the possible target display's for the adapters
        DisplayCount[Index] = 0;
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hDevices[Index], &DisplayCount[Index], hDisplayOutput[Index]));
        hDisplayOutput[Index] = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * DisplayCount[Index]);
        NULL_PTR_CHECK(hDisplayOutput[Index]);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[Index], &DisplayCount[Index], hDisplayOutput[Index]);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput[Index]);
            FREE_MEMORY(hDevices);
            return apiResult;
        }
    }

    if (handle == nullptr)
    {
        MuxCount = 0;
        VERIFY_API_STATUS(ControlApiEnumerateMuxDevices(apiContext.apiHandle, &MuxCount, hMuxDevices));
        hMuxDevices = (ctl_mux_output_handle_t *)malloc(sizeof(ctl_mux_output_handle_t) * MuxCount);
        NULL_PTR_CHECK(hMuxDevices);
        apiResult = ControlApiEnumerateMuxDevices(apiContext.apiHandle, &MuxCount, hMuxDevices);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateMuxDevices Failed!!");
            FREE_MEMORY(hMuxDevices);
            return apiResult;
        }
        if (MuxCount > 1)
        {
            ERROR_LOG("Only 1 MUX expected for now, in future will implement > 1 MUX devices as needed");
            apiResult = FALSE;
            return apiResult;
        }
        handle = (ctl_mux_output_handle_t *)malloc(sizeof(ctl_mux_output_handle_t) * MuxCount);
        memcpy(handle, hMuxDevices, sizeof(hMuxDevices));
    }

    ZeroMemory(&MuxProperties, sizeof(MuxProperties));
    VERIFY_API_STATUS(ControlApiGetMuxProperties(handle[0], &MuxProperties));

    if (MuxProperties.Count != 2)
    {
        ERROR_LOG("Invalid number of display outputs on the MUX device!!");
        apiResult = FALSE;
        return apiResult;
    }
    MuxProperties.phDisplayOutputs = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * MuxProperties.Count);
    NULL_PTR_CHECK(handle);
    apiResult = ControlApiGetMuxProperties(handle[0], &MuxProperties);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API GetMuxProperties Failed!!");
        FREE_MEMORY(MuxProperties.phDisplayOutputs);
        return apiResult;
    }

    if (MuxProperties.IndexOfDisplayOutputOwningMux == 0xFF)
    {
        ERROR_LOG("No DisplayOutput on the Mux is active, Display Switching is not possible");
        apiResult = FALSE;
        return apiResult;
    }

    ActiveDisplayOut = MuxProperties.phDisplayOutputs[MuxProperties.IndexOfDisplayOutputOwningMux];
    for (Index = 0; Index < MuxProperties.Count; Index++)
    {
        if (MuxProperties.IndexOfDisplayOutputOwningMux != Index)
        {
            InActiveDisplayOutput = MuxProperties.phDisplayOutputs[Index];
        }
    }

    apiResult = ControlApiSwitchMux(handle[0], InActiveDisplayOutput);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Switch Mux Failed!!");
        return apiResult;
    }

    INFO_LOG("Overrall test result is %d", apiResult);
    return apiResult;
}

bool ControlAPIGetDisplayEncoderProperties(ctl_adapter_display_encoder_properties_t *displayEncoderProperties, PANEL_INFO *pPanelInfo)
{
    bool                                     apiResult            = TRUE;
    bool                                     displayAdapterStatus = TRUE;
    uint32_t                                 displayIndex         = 0;
    uint32_t                                 adapterIndex         = 0;
    uint32_t                                 displayCount         = 0;
    uint32_t                                 adapterCount         = 0;
    ctl_device_adapter_handle_t *            hDevices             = nullptr;
    ctl_device_adapter_handle_t *            hActDevices          = nullptr;
    ctl_display_output_handle_t *            hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *            hDisplayActive       = nullptr;
    ctl_adapter_display_encoder_properties_t displayEncoderArgs   = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("ControlApiEnumerateDevices Failed!!");
        FREE_MEMORY(hDevices);
        FREE_MEMORY(hActDevices);
        return FALSE;
    }

    if (TRUE != GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID))
    {
        ERROR_LOG("ControlApiGetDisplayEncoderProperties Failed !!!");
        goto END;
    }
    DEBUG_LOG("ControlAPIGetDisplayEncoderProperties adapterCount %d ", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        displayCount = 0;
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);

        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            displayAdapterStatus &= apiResult;
        }

        if (TRUE == displayAdapterStatus)
        {
            if (TRUE != GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID))
            {
                ERROR_LOG("Failed to get Active Displays during ControlAPIGetDisplayEncoderProperties Call !!!");
                goto END;
            }
            DEBUG_LOG("ControlAPIGetDisplayEncoderProperties displayCount %d ", displayCount);
            displayEncoderArgs.Size = sizeof(ctl_adapter_display_encoder_properties_t);

            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiGetDisplayEncoderProperties(hDisplayActive[displayIndex], &displayEncoderArgs);

                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetDisplayProperties Failed");
                    displayAdapterStatus &= apiResult;
                }
                else
                {
                    INFO_LOG("Display TargetID %d", displayEncoderArgs.Os_display_encoder_handle.WindowsDisplayEncoderID);
                    DEBUG_LOG("Type %d", displayEncoderArgs.Type);
                    DEBUG_LOG("IsOnBoardProtocolConverterOutputPresent %d", displayEncoderArgs.IsOnBoardProtocolConverterOutputPresent);
                    DEBUG_LOG("SupportedSpec: Major - %d, Minor - %d, Revision - %d ", displayEncoderArgs.SupportedSpec.major_version,
                              displayEncoderArgs.SupportedSpec.minor_version, displayEncoderArgs.SupportedSpec.revision_version);
                    DEBUG_LOG("SupportedOutputBPCFlags %d", displayEncoderArgs.SupportedOutputBPCFlags);
                    DEBUG_LOG("EncoderConfigFlags %d", displayEncoderArgs.EncoderConfigFlags);
                    DEBUG_LOG("FeatureSupportedFlags %d", displayEncoderArgs.FeatureSupportedFlags);
                    DEBUG_LOG("AdvancedFeatureSupportedFlags %d", displayEncoderArgs.AdvancedFeatureSupportedFlags);
                    memcpy(displayEncoderProperties, &displayEncoderArgs, sizeof(ctl_adapter_display_encoder_properties_t));
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return displayAdapterStatus;
}

bool ControlAPIGetDeviceProperties(ctl_device_adapter_properties_t *deviceProperties, PANEL_INFO *pPanelInfo)
{
    ctl_device_adapter_properties_t deviceAdapterProperties = { 0 };
    uint32_t                        adapterIndex            = 0;
    uint32_t                        adapterCount            = 0;
    ctl_device_adapter_handle_t *   hDevices                = nullptr;
    ctl_device_adapter_handle_t *   hActDevices             = nullptr;
    bool                            apiResult               = TRUE;
    LUID                            adapterID;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetDeviceProperties !!!");
        goto END;
    }

    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        if (NULL != hActDevices[adapterIndex])
        {
            deviceAdapterProperties.Size      = deviceProperties->Size;
            deviceAdapterProperties.pDeviceID = malloc(sizeof(LUID));
            NULL_PTR_CHECK(deviceAdapterProperties.pDeviceID);
            deviceAdapterProperties.device_id_size = sizeof(LUID);

            VERIFY_API_STATUS(ControlApiGetDeviceProperties(hActDevices[adapterIndex], &deviceAdapterProperties));

            if (CTL_DEVICE_TYPE_GRAPHICS != deviceAdapterProperties.device_type)
            {
                DEBUG_LOG("This is not a Graphics Device \n");
                FREE_MEMORY(deviceAdapterProperties.pDeviceID);
                continue;
            }

            adapterID = *(reinterpret_cast<LUID *>(deviceAdapterProperties.pDeviceID));

            if (INTEL_VENDOR_ID == deviceAdapterProperties.pci_vendor_id)
            {
                DEBUG_LOG("Intel Adapter Name %s", deviceAdapterProperties.name);
                DEBUG_LOG("Vendor ID %d", deviceAdapterProperties.pci_vendor_id);
                DEBUG_LOG("Device ID %d", deviceAdapterProperties.pci_device_id);
                DEBUG_LOG("Rev ID %d", deviceAdapterProperties.rev_id);
                DEBUG_LOG("Adapter ID %d", adapterID.LowPart);
                DEBUG_LOG("Firmware Version Build-%d, Major-%d, Minor-%d", deviceAdapterProperties.firmware_version.build_number,
                          deviceAdapterProperties.firmware_version.major_version, deviceAdapterProperties.firmware_version.minor_version);
                memcpy(deviceProperties, &deviceAdapterProperties, sizeof(ctl_device_adapter_properties_t));
            }
        }
    }
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(deviceAdapterProperties.pDeviceID);
    return apiResult;
}

bool ControlAPIGetZeDevice(ze_device_module_properties_t *zeProperties)
{
    uint32_t                      adapterCount = 0;
    ctl_device_adapter_handle_t * hDevices     = nullptr;
    bool                          apiResult    = TRUE;
    ze_device_handle_t            zeDevice;
    ze_device_module_properties_t zemoduleProperties;
    HINSTANCE                     hLevel0Loader = NULL;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        FREE_MEMORY(hDevices);
        return apiResult;
    }

    if (adapterCount > 0)
    {
        for (unsigned int i = 0; i < adapterCount; i++)
        {
            VERIFY_API_STATUS(ControlApiGetZeDevice(hDevices[i], &zeDevice, &(void *)hLevel0Loader));

            NULL_PTR_CHECK(zeDevice);
            NULL_PTR_CHECK(hLevel0Loader);
            ze_pfnDeviceGetModuleProperties_t pfnDeviceGetModuleProperties = (ze_pfnDeviceGetModuleProperties_t)GetProcAddress(hLevel0Loader, "zeDeviceGetModuleProperties");
            NULL_PTR_CHECK(pfnDeviceGetModuleProperties);
            INFO_LOG("Success: Obtained level0 handle for zeDeviceGetModuleProperties");

            if (pfnDeviceGetModuleProperties(zeDevice, &zemoduleProperties) == ZE_RESULT_SUCCESS)
            {
                INFO_LOG("zeDeviceGetModuleProperties-spirvVersionSupported %d", zemoduleProperties.spirvVersionSupported);
                memcpy(zeProperties, &zemoduleProperties, sizeof(ze_device_module_properties_t));
            }
            else
            {
                ERROR_LOG("pfnDeviceGetModuleProperties() returned failure");
                FREE_MEMORY(hDevices);
                apiResult = FALSE;
                return apiResult;
            }

            FreeLibrary(hLevel0Loader);
        }
    }
    FREE_MEMORY(hDevices);
    return apiResult;
}

bool ControlAPII2CAccess(ctl_i2c_access_args_t *argsi2c, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult            = TRUE;
    bool                         displayAdapterStatus = TRUE;
    uint32_t                     adapterIndex         = 0;
    uint32_t                     adapterCount         = 0;
    uint32_t                     displayCount         = 0;
    uint32_t                     displayIndex         = 0;
    ctl_device_adapter_handle_t *hDevices             = nullptr;
    ctl_device_adapter_handle_t *hActDevices          = nullptr;
    ctl_display_output_handle_t *hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *hDisplayActive       = nullptr;
    ctl_i2c_access_args_t        I2CArgs              = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    if (TRUE != GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID))
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPII2CAccess !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during I2CAccess Call !!!");
            goto END;
        }
        DEBUG_LOG("I2CAccess: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                if (CTL_OPERATION_TYPE_WRITE == argsi2c->OpType)
                {
                    I2CArgs.Size     = sizeof(ctl_i2c_access_args_t);
                    I2CArgs.OpType   = argsi2c->OpType;
                    I2CArgs.Address  = argsi2c->Address;
                    I2CArgs.Offset   = argsi2c->Offset;
                    I2CArgs.DataSize = argsi2c->DataSize;
                    I2CArgs.Data[0]  = argsi2c->Data[0];
                    I2CArgs.Data[1]  = argsi2c->Data[1];
                    I2CArgs.Data[2]  = argsi2c->Data[2];
                    I2CArgs.Data[3]  = argsi2c->Data[3];

                    // Log the data for debug
                    for (uint32_t data_index = 0; data_index < I2CArgs.DataSize; data_index++)
                    {
                        INFO_LOG("Write data[%d] = : 0x%X\n", data_index, I2CArgs.Data[data_index]);
                    }

                    VERIFY_API_STATUS(ControlApiI2cAccess(hDisplayActive[displayIndex], &I2CArgs));
                    DEBUG_LOG("Control API I2C Write Success");
                }
                else
                {
                    I2CArgs.Size     = sizeof(ctl_i2c_access_args_t);
                    I2CArgs.OpType   = argsi2c->OpType;
                    I2CArgs.Address  = argsi2c->Address;
                    I2CArgs.Offset   = argsi2c->Offset;
                    I2CArgs.DataSize = argsi2c->DataSize;
                    I2CArgs.Flags    = argsi2c->Flags; // Set to Atomic I2C if Atomic call

                    VERIFY_API_STATUS(ControlApiI2cAccess(hDisplayActive[displayIndex], &I2CArgs));
                    // Log the data for debug
                    for (uint32_t data_index = 0; data_index < I2CArgs.DataSize; data_index++)
                    {
                        INFO_LOG("Read data[%d] = : 0x%X\n", data_index, I2CArgs.Data[data_index]);
                    }
                    memcpy_s(&argsi2c->Data, argsi2c->DataSize, I2CArgs.Data, I2CArgs.DataSize);
                    DEBUG_LOG("Control API I2C Read Success");
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIAuxAccess(ctl_aux_access_args_t *auxargs, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_aux_access_args_t        AUXArgs        = { 0 };

    NULL_PTR_CHECK(pPanelInfo);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIAuxAccess !!!");
        goto END;
    }

    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during AuxAccess Call !!!");
            goto END;
        }
        DEBUG_LOG("AuxAccess: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                if (CTL_OPERATION_TYPE_WRITE == auxargs->OpType)
                {
                    // AUX Access WRITE
                    AUXArgs.Size     = auxargs->Size;
                    AUXArgs.OpType   = auxargs->OpType;
                    AUXArgs.Address  = auxargs->Address;
                    AUXArgs.DataSize = auxargs->DataSize;
                    AUXArgs.Flags    = auxargs->Flags;
                    AUXArgs.Data[0]  = auxargs->Data[0];
                    // Log the data for debug
                    for (uint32_t data_index = 0; data_index < AUXArgs.DataSize; data_index++)
                    {
                        INFO_LOG("Write data[%d] = : 0x%X\n", data_index, AUXArgs.Data[data_index]);
                    }
                    VERIFY_API_STATUS(ControlApiAuxAccess(hDisplayActive[displayIndex], &AUXArgs));
                    DEBUG_LOG("Control API Aux Write Success");
                }
                else
                {
                    // AUX Access READ
                    AUXArgs.Size     = auxargs->Size;
                    AUXArgs.OpType   = auxargs->OpType;
                    AUXArgs.Address  = auxargs->Address;
                    AUXArgs.DataSize = auxargs->DataSize;
                    AUXArgs.Flags    = auxargs->Flags;

                    VERIFY_API_STATUS(ControlApiAuxAccess(hDisplayActive[displayIndex], &AUXArgs));
                    // Log the data for debug
                    for (uint32_t data_index = 0; data_index < AUXArgs.DataSize; data_index++)
                    {
                        INFO_LOG("Read data[%d] = : 0x%X\n", data_index, AUXArgs.Data[data_index]);
                    }
                    memcpy_s(&auxargs->Data, auxargs->DataSize, AUXArgs.Data, AUXArgs.DataSize);
                    DEBUG_LOG("Control API Aux Read Success");
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetSharpnessCaps(ctl_sharpness_caps_t *getSharpnessCaps, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_sharpness_caps_t         sharpnessCaps  = { 0 };

    sharpnessCaps.Size = sizeof(ctl_sharpness_caps_t);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetSharpnessCaps !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during SharpnessCaps Call !!!");
            goto END;
        }
        DEBUG_LOG("SharpnessCaps: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            // Get Sharpness Caps
            if (NULL != hDisplayActive[displayIndex])
            {
                VERIFY_API_STATUS(ControlApiGetSharpnessCaps(hDisplayActive[displayIndex], &sharpnessCaps));

                sharpnessCaps.pFilterProperty = (ctl_sharpness_filter_properties_t *)malloc(sharpnessCaps.NumFilterTypes * sizeof(ctl_sharpness_filter_properties_t));
                NULL_PTR_CHECK(sharpnessCaps.pFilterProperty);
                apiResult = ControlApiGetSharpnessCaps(hDisplayOutput[0], &sharpnessCaps);

                if (FALSE == apiResult)
                {
                    ERROR_LOG("ctlGetSharpnessCaps failed to get caps after malloc\n");
                    FREE_MEMORY(sharpnessCaps.pFilterProperty);
                    goto END;
                }

                DEBUG_LOG("sharpnessCaps.SupportedFilterFlags = %d\n", sharpnessCaps.SupportedFilterFlags);
                DEBUG_LOG("sharpnessCaps.NumFilterTypes = %d\n", sharpnessCaps.NumFilterTypes);

                for (int num_filter = 0; num_filter < sharpnessCaps.NumFilterTypes; num_filter++)
                {
                    DEBUG_LOG(" sharpnessCaps.pFilterProperty[%d].FilterType = %d\n", num_filter, sharpnessCaps.pFilterProperty[num_filter].FilterType);
                    DEBUG_LOG(" sharpnessCaps.pFilterProperty[%d].FilterDetails.min_possible_value = %f\n", num_filter,
                              sharpnessCaps.pFilterProperty[num_filter].FilterDetails.min_possible_value);
                    DEBUG_LOG(" sharpnessCaps.pFilterProperty[%d].FilterDetails.max_possible_value = %f\n", num_filter,
                              sharpnessCaps.pFilterProperty[num_filter].FilterDetails.max_possible_value);
                    DEBUG_LOG(" sharpnessCaps.pFilterProperty[%d].FilterDetails.step_size = %f\n", num_filter, sharpnessCaps.pFilterProperty[num_filter].FilterDetails.step_size);
                }
                memcpy(getSharpnessCaps, &sharpnessCaps, sizeof(ctl_sharpness_caps_t));
                FREE_MEMORY(sharpnessCaps.pFilterProperty);
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetCurrentSharpness(ctl_sharpness_settings_t *setSharpness, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_sharpness_caps_t         sharpnessCaps  = { 0 };
    ctl_sharpness_settings_t     SetSharpness   = { 0 };

    sharpnessCaps.Size = sizeof(ctl_sharpness_caps_t);

    SetSharpness.FilterType = setSharpness->FilterType;
    SetSharpness.Enable     = setSharpness->Enable;
    SetSharpness.Intensity  = setSharpness->Intensity;
    SetSharpness.Size       = setSharpness->Size;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetCurrentSharpness !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during SetSharpness Call !!!");
            goto END;
        }
        DEBUG_LOG("SetSharpness: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            // Get Sharpness Caps
            if (NULL != hDisplayActive[displayIndex])
            {
                VERIFY_API_STATUS(ControlApiGetSharpnessCaps(hDisplayActive[displayIndex], &sharpnessCaps));

                sharpnessCaps.pFilterProperty = (ctl_sharpness_filter_properties_t *)malloc(sharpnessCaps.NumFilterTypes * sizeof(ctl_sharpness_filter_properties_t));
                NULL_PTR_CHECK(sharpnessCaps.pFilterProperty);

                apiResult = ControlApiGetSharpnessCaps(hDisplayActive[displayIndex], &sharpnessCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ctlGetSharpnessCaps failed to get caps after malloc\n");
                    FREE_MEMORY(sharpnessCaps.pFilterProperty);
                    goto END;
                }

                DEBUG_LOG("sharpnessCaps.SupportedFilterFlags = %d\n", sharpnessCaps.SupportedFilterFlags);

                if (TRUE == apiResult && ((sharpnessCaps.SupportedFilterFlags == CTL_SHARPNESS_FILTER_TYPE_FLAG_NON_ADAPTIVE) ||
                                          (sharpnessCaps.SupportedFilterFlags == CTL_SHARPNESS_FILTER_TYPE_FLAG_ADAPTIVE)))
                {
                    // SetSharpness
                    if (NULL != hDisplayActive[displayIndex])
                    {
                        VERIFY_API_STATUS(ControlApiSetCurrentSharpness(hDisplayActive[displayIndex], &SetSharpness));
                    }
                }
                FREE_MEMORY(sharpnessCaps.pFilterProperty);
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetCurrentSharpness(ctl_sharpness_settings_t *getSharpness, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_sharpness_settings_t     GetSharpness   = { 0 };

    GetSharpness.Size = sizeof(ctl_sharpness_settings_t);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetCurrentSharpness !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during GetSharpness Call !!!");
            goto END;
        }
        DEBUG_LOG("GetSharpness: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            // GetSharpness
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiGetCurrentSharpness(hDisplayActive[displayIndex], &GetSharpness);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("Control API GetCurrentSharpness Failed!!");
                    goto END;
                }
                DEBUG_LOG("ControlApiGetCurrentSharpness call success\n");
                DEBUG_LOG("GetSharpness.Enable = %d\n", GetSharpness.Enable);
                DEBUG_LOG("GetSharpness.FilterType = %d\n", GetSharpness.FilterType);
                DEBUG_LOG("GetSharpness.Intensity = %f\n", GetSharpness.Intensity);
                memcpy(getSharpness, &GetSharpness, sizeof(ctl_sharpness_settings_t));
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetPanelDescriptorAccess(ctl_panel_descriptor_access_args_t *argsPanelDesc, ctl_panel_descriptor_access_args_t *argsExtBlockPanelDesc, PANEL_INFO *pPanelInfo,
                                        BYTE edidData[])
{
    bool                               apiResult             = TRUE;
    uint32_t                           adapterIndex          = 0;
    uint32_t                           adapterCount          = 0;
    uint32_t                           displayCount          = 0;
    uint32_t                           displayIndex          = 0;
    uint8_t                            NumberOfExtnBlocks    = 0;
    ctl_device_adapter_handle_t *      hDevices              = nullptr;
    ctl_device_adapter_handle_t *      hActDevices           = nullptr;
    ctl_display_output_handle_t *      hDisplayOutput        = nullptr;
    ctl_display_output_handle_t *      hDisplayActive        = nullptr;
    ctl_panel_descriptor_access_args_t PanelDescArgs         = { 0 };
    ctl_panel_descriptor_access_args_t ExtBlockPanelDescArgs = { 0 };

    PanelDescArgs.Size               = argsPanelDesc->Size;
    PanelDescArgs.OpType             = argsPanelDesc->OpType;
    PanelDescArgs.BlockNumber        = argsPanelDesc->BlockNumber;
    PanelDescArgs.DescriptorDataSize = 0;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetPanelDescriptorAccess !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during GetPanelDescriptorAccess Call !!!");
            goto END;
        }
        DEBUG_LOG("GetPanelDescriptorAccess: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                VERIFY_API_STATUS(ControlApiPanelDescriptorAccess(hDisplayActive[displayIndex], &PanelDescArgs));

                argsPanelDesc->DescriptorDataSize = PanelDescArgs.DescriptorDataSize;
                DEBUG_LOG("Control API Panel Descriptor DataSize Call Success");
                DEBUG_LOG("DescriptorDataSize = %d\n", PanelDescArgs.DescriptorDataSize);
                PanelDescArgs.pDescriptorData = (uint8_t *)malloc(PanelDescArgs.DescriptorDataSize * sizeof(uint8_t));
                NULL_PTR_CHECK(PanelDescArgs.pDescriptorData);

                apiResult = ControlApiPanelDescriptorAccess(hDisplayActive[displayIndex], &PanelDescArgs);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("Control API PanelDescriptorAccess Failed!!");
                    FREE_MEMORY(PanelDescArgs.pDescriptorData);
                    goto END;
                }
                DEBUG_LOG("Control API Panel Descriptor Data Call Success");

                for (uint32_t data = 0; data < PanelDescArgs.DescriptorDataSize; data++)
                {
                    DEBUG_LOG("EDID Data [%d] = : 0x%X\n", data, PanelDescArgs.pDescriptorData[data]);
                }

                DEBUG_LOG("Control API Panel Descriptor Data Call Success");
                DEBUG_LOG("Control API Panel Descriptor Size %d ", PanelDescArgs.DescriptorDataSize);
                memcpy_s(edidData, EDID_BLOCK_SIZE, PanelDescArgs.pDescriptorData, EDID_BLOCK_SIZE);

                // EXTENSION BLOCKS READ : Need to get the number of extensions blocks from 127th byte (Number of extension blocks) of base block
                NumberOfExtnBlocks = PanelDescArgs.pDescriptorData[EXTENSIONS_BYTE];

                if (NumberOfExtnBlocks > 0)
                {
                    DEBUG_LOG("Control API Panel Descriptor for Extension Block Read");
                    for (uint32_t block_count = 1; block_count <= NumberOfExtnBlocks; block_count++)
                    {
                        ExtBlockPanelDescArgs.Size               = sizeof(ctl_panel_descriptor_access_args_t);
                        ExtBlockPanelDescArgs.OpType             = CTL_OPERATION_TYPE_READ;
                        ExtBlockPanelDescArgs.BlockNumber        = block_count;
                        ExtBlockPanelDescArgs.DescriptorDataSize = 0;
                        VERIFY_API_STATUS(ControlApiPanelDescriptorAccess(hDisplayActive[displayIndex], &ExtBlockPanelDescArgs));

                        DEBUG_LOG("Control API Panel Descriptor DataSize Call for Extension block Success");
                        DEBUG_LOG("DescriptorDataSize for extension block = : %d\n", ExtBlockPanelDescArgs.DescriptorDataSize);

                        argsExtBlockPanelDesc->DescriptorDataSize = ExtBlockPanelDescArgs.DescriptorDataSize;
                        ExtBlockPanelDescArgs.pDescriptorData     = (uint8_t *)malloc(ExtBlockPanelDescArgs.DescriptorDataSize * sizeof(uint8_t));
                        NULL_PTR_CHECK(ExtBlockPanelDescArgs.pDescriptorData);

                        apiResult = ControlApiPanelDescriptorAccess(hDisplayActive[displayIndex], &ExtBlockPanelDescArgs);
                        if (FALSE == apiResult)
                        {
                            ERROR_LOG("ControlApiPanelDescriptorAccess for extension block %d returned failure code: 0x%X\n", block_count, apiResult);
                            FREE_MEMORY(ExtBlockPanelDescArgs.pDescriptorData);
                            goto END;
                        }
                        DEBUG_LOG("Control API Panel Descriptor Data Call for Extension block Success");

                        for (uint32_t data = 0; data < ExtBlockPanelDescArgs.DescriptorDataSize; data++)
                        {
                            DEBUG_LOG("EDID Data [%d] = : 0x%X\n", data, ExtBlockPanelDescArgs.pDescriptorData[data]);
                        }

                        DEBUG_LOG("Control API Panel Descriptor Data Call for Extension block Success");
                        memcpy_s((edidData + (block_count * EDID_BLOCK_SIZE)), (block_count * EDID_BLOCK_SIZE), ExtBlockPanelDescArgs.pDescriptorData, EDID_BLOCK_SIZE);

                        FREE_MEMORY(ExtBlockPanelDescArgs.pDescriptorData);
                    }
                }
            }
            FREE_MEMORY(PanelDescArgs.pDescriptorData);
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetPowerCaps(ctl_power_optimization_caps_t *argsGetPowerCaps, PANEL_INFO *pPanelInfo)
{
    bool                          apiResult      = TRUE;
    uint32_t                      adapterIndex   = 0;
    uint32_t                      adapterCount   = 0;
    uint32_t                      displayCount   = 0;
    uint32_t                      displayIndex   = 0;
    ctl_device_adapter_handle_t * hDevices       = nullptr;
    ctl_device_adapter_handle_t * hActDevices    = nullptr;
    ctl_display_output_handle_t * hDisplayOutput = nullptr;
    ctl_display_output_handle_t * hDisplayActive = nullptr;
    ctl_power_optimization_caps_t getPowerCaps   = { 0 };

    getPowerCaps.Size = argsGetPowerCaps->Size;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetPowerCaps !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetPowerCaps: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ctlGetPowerOptimizationCaps Query Passed\n");

                switch (getPowerCaps.SupportedFeatures)
                {
                case CTL_POWER_OPTIMIZATION_FLAG_FBC:
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = CTL_POWER_OPTIMIZATION_FLAG_FBC \n");
                    break;
                case CTL_POWER_OPTIMIZATION_FLAG_PSR:
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = PSR \n");
                    break;
                case (CTL_POWER_OPTIMIZATION_FLAG_FBC | CTL_POWER_OPTIMIZATION_FLAG_PSR):
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = PSR / FBC \n");
                    break;
                case CTL_POWER_OPTIMIZATION_FLAG_DPST:
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = CTL_POWER_OPTIMIZATION_FLAG_DPST \n");
                    break;
                case (CTL_POWER_OPTIMIZATION_FLAG_FBC | CTL_POWER_OPTIMIZATION_FLAG_DPST):
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = FBC / DPST \n");
                    break;
                case (CTL_POWER_OPTIMIZATION_FLAG_PSR | CTL_POWER_OPTIMIZATION_FLAG_DPST):
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = PSR / DPST \n");
                    break;
                case (CTL_POWER_OPTIMIZATION_FLAG_PSR | CTL_POWER_OPTIMIZATION_FLAG_FBC | CTL_POWER_OPTIMIZATION_FLAG_DPST):
                    INFO_LOG("GetPowerOptimizationCaps.SupportedFeature = PSR / FBC / DPST \n");
                    break;
                default:
                    ERROR_LOG("Power Feature not Supported \n");
                }
                memcpy_s(argsGetPowerCaps, argsGetPowerCaps->Size, &getPowerCaps, getPowerCaps.Size);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetPSR(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t setPowerSettings = { 0 };
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;

    NULL_PTR_CHECK(argsSetPowerSettings);
    getPowerCaps.Size                         = sizeof(ctl_power_optimization_caps_t);
    setPowerSettings.Size                     = sizeof(ctl_power_optimization_settings_t);
    setPowerSettings.PowerOptimizationFeature = CTL_POWER_OPTIMIZATION_FLAG_PSR;
    setPowerSettings.PowerOptimizationPlan    = argsSetPowerSettings->PowerOptimizationPlan;
    setPowerSettings.PowerSource              = argsSetPowerSettings->PowerSource;
    setPowerSettings.Enable                   = argsSetPowerSettings->Enable;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetPSR !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!\n");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPISetPSR: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getPowerCaps.Size = sizeof(ctl_power_optimization_caps_t);
                apiResult         = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ctlGetPowerOptimizationCaps Query Passed\n");

                if (TRUE == apiResult && (CTL_POWER_OPTIMIZATION_FLAG_PSR & getPowerCaps.SupportedFeatures))
                {
                    apiResult = ControlApiSetPowerOptimizationSetting(hDisplayActive[displayIndex], &setPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiSetPowerOptimizationSetting Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    DEBUG_LOG("ctlSetPowerOptimizationSetting returned success\n");
                    DEBUG_LOG("PSR SetPowerSettings.Enable = %d\n", setPowerSettings.Enable);
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetPSR(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t getPowerSettings = { 0 };

    getPowerCaps.Size                         = sizeof(ctl_power_optimization_caps_t);
    getPowerSettings.Size                     = sizeof(ctl_power_optimization_settings_t);
    getPowerSettings.PowerOptimizationFeature = CTL_POWER_OPTIMIZATION_FLAG_PSR;
    getPowerSettings.PowerOptimizationPlan    = argsGetPowerSettings->PowerOptimizationPlan;
    getPowerSettings.PowerSource              = argsGetPowerSettings->PowerSource;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetPSR !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetPSR: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps Call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetPowerOptimizationCaps Query Passed\n");

                if (TRUE == apiResult && (CTL_POWER_OPTIMIZATION_FLAG_PSR & getPowerCaps.SupportedFeatures))
                {
                    apiResult = ControlApiGetPowerOptimizationSetting(hDisplayActive[displayIndex], &getPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiGetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }
                    memcpy_s(argsGetPowerSettings, argsGetPowerSettings->Size, &getPowerSettings, getPowerSettings.Size);

                    DEBUG_LOG("ControlApiGetPowerOptimizationSetting Call Passed\n");
                    DEBUG_LOG("PSR GetPowerSettings.Enable = %d\n", getPowerSettings.Enable);
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetUBRR(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t setPowerSettings = { 0 };
    ctl_power_optimization_settings_t disablePSR       = { 0 };
    ctl_power_optimization_settings_t getPowerSettings = { 0 };
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;

    NULL_PTR_CHECK(argsSetPowerSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetUBRR !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!\n");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPISetUBRR: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getPowerCaps.Size = sizeof(ctl_power_optimization_caps_t);
                apiResult         = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps call failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ctlGetPowerOptimizationCaps Query Passed\n");

                if (TRUE == apiResult && (getPowerCaps.SupportedFeatures & CTL_POWER_OPTIMIZATION_FLAG_LRR))
                {
                    getPowerSettings.PowerOptimizationFeature = CTL_POWER_OPTIMIZATION_FLAG_LRR;
                    getPowerSettings.Size                     = sizeof(ctl_power_optimization_settings_t);
                    apiResult                                 = ControlApiGetPowerOptimizationSetting(hDisplayActive[displayIndex], &getPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiGetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    if (getPowerSettings.FeatureSpecificData.LRRInfo.SupportedLRRTypes & argsSetPowerSettings->FeatureSpecificData.LRRInfo.CurrentLRRTypes)
                    {
                        if (getPowerSettings.FeatureSpecificData.LRRInfo.bRequirePSRDisable)
                        {
                            if (TRUE == apiResult && (CTL_POWER_OPTIMIZATION_FLAG_PSR & getPowerCaps.SupportedFeatures))
                            {
                                // Disable PSR
                                disablePSR.Size                     = sizeof(ctl_power_optimization_settings_t);
                                disablePSR.PowerOptimizationFeature = CTL_POWER_OPTIMIZATION_FLAG_PSR;
                                disablePSR.Enable                   = FALSE;

                                apiResult = ControlApiSetPowerOptimizationSetting(hDisplayActive[displayIndex], &disablePSR);
                                if (FALSE == apiResult)
                                {
                                    ERROR_LOG("ControlApiSetPowerOptimizationSetting Disable PSR Failed : 0x%X\n", apiResult);
                                    goto END;
                                }
                                DEBUG_LOG("ControlApiSetPowerOptimizationSetting PSR is Disabled\n");
                            }
                        }
                        setPowerSettings.Size                                        = argsSetPowerSettings->Size;
                        setPowerSettings.PowerOptimizationFeature                    = argsSetPowerSettings->PowerOptimizationFeature;
                        setPowerSettings.Enable                                      = argsSetPowerSettings->Enable;
                        setPowerSettings.FeatureSpecificData.LRRInfo.CurrentLRRTypes = argsSetPowerSettings->FeatureSpecificData.LRRInfo.CurrentLRRTypes;
                        apiResult                                                    = ControlApiSetPowerOptimizationSetting(hDisplayActive[displayIndex], &setPowerSettings);
                        if (FALSE == apiResult)
                        {
                            ERROR_LOG("ControlApiSetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                            goto END;
                        }
                        DEBUG_LOG("ControlApiSetPowerOptimizationSetting for UBRR Passed\n");
                    }

                    DEBUG_LOG("ControlAPISetUBRR - UBRR Passed\n");
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetUBRR(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t getPowerSettings = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetUBRR !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetUBRR: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getPowerCaps.Size = sizeof(ctl_power_optimization_caps_t);
                apiResult         = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps Call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetPowerOptimizationCaps Query Call Passed\n");

                if (TRUE == apiResult && (getPowerCaps.SupportedFeatures & CTL_POWER_OPTIMIZATION_FLAG_LRR))
                {
                    getPowerSettings.Size                     = sizeof(ctl_power_optimization_settings_t);
                    getPowerSettings.PowerOptimizationFeature = argsGetPowerSettings->PowerOptimizationFeature;
                    apiResult                                 = ControlApiGetPowerOptimizationSetting(hDisplayActive[displayIndex], &getPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiGetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }
                    memcpy_s(argsGetPowerSettings, argsGetPowerSettings->Size, &getPowerSettings, getPowerSettings.Size);

                    DEBUG_LOG("ControlApiGetPowerOptimizationSetting Call Passed\n");
                    DEBUG_LOG("UBRR GetPowerSettings.Enable = %d\n", getPowerSettings.Enable);
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIColorGetCapability(ctl_pixtx_pipe_get_config_t *argsGetConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelGetConfig = { 0 };
    pixelGetConfig.QueryType                    = argsGetConfig->QueryType;
    pixelGetConfig.Size                         = argsGetConfig->Size;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIColorGetCapability !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during GetCapability Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIColorGetCapability: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelGetConfig);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelGetConfig.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Passed for NumBlocks - %d\n", pixelGetConfig.NumBlocks);
                const uint32_t blocksToQuery = pixelGetConfig.NumBlocks;
                pixelGetConfig.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelGetConfig.pBlockConfigs)
                {
                    memset(pixelGetConfig.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelGetConfig);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for BlockType : 0x%X\n", apiResult);
                        goto END;
                    }
                    for (uint32_t blockId = 0; blockId < pixelGetConfig.NumBlocks; blockId++)
                    {
                        // Block specific information
                        INFO_LOG("pixelGetConfig->pBlockConfigs[%d].BlockId = %d\n", blockId, pixelGetConfig.pBlockConfigs[blockId].BlockId);

                        if (CTL_PIXTX_BLOCK_TYPE_3D_LUT == pixelGetConfig.pBlockConfigs[blockId].BlockType)
                        {
                            INFO_LOG("Block Type is CTL_PIXTX_BLOCK_TYPE_3D_LUT\n");
                        }

                        if (CTL_PIXTX_BLOCK_TYPE_1D_LUT == pixelGetConfig.pBlockConfigs[blockId].BlockType)
                        {
                            INFO_LOG("Block Type is CTL_PIXTX_BLOCK_TYPE_1D_LUT\n");
                            INFO_LOG("pixelGetConfig->pBlockConfigs[%d].Config.OneDLutConfig.NumChannels = %d\n", blockId,
                                     pixelGetConfig.pBlockConfigs[blockId].Config.OneDLutConfig.NumChannels);
                            INFO_LOG("pixelGetConfig->pBlockConfigs[%d].Config.OneDLutConfig.NumSamplesPerChannel = %d\n", blockId,
                                     pixelGetConfig.pBlockConfigs[blockId].Config.OneDLutConfig.NumSamplesPerChannel);
                            INFO_LOG("pixelGetConfig->pBlockConfigs[%d].Config.OneDLutConfig.SamplingType = %d\n", blockId,
                                     pixelGetConfig.pBlockConfigs[blockId].Config.OneDLutConfig.SamplingType);
                        }
                        else if (CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX == pixelGetConfig.pBlockConfigs[blockId].BlockType)
                        {
                            INFO_LOG("Block type is CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX\n");
                            INFO_LOG("pixelGetConfig->pBlockConfigs[%d].Config.ThreeDLutConfig.NumSamplesPerChannel = %d\n", blockId,
                                     pixelGetConfig.pBlockConfigs[blockId].Config.ThreeDLutConfig.NumSamplesPerChannel);
                        }
                    }
                }
            }
        }
        memcpy_s(argsGetConfig, sizeof(ctl_pixtx_pipe_get_config_t), &pixelGetConfig, sizeof(pixelGetConfig));
    }

END:
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool GetGamma(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pPixelConfigCaps, int32_t oneDLUTIndex, ctl_pixtx_block_config_t *argsLutConfig)
{
    bool                        apiResult        = TRUE;
    uint32_t                    lutDataSize      = 0;
    uint32_t                    sampleValueIndex = 0;
    ctl_pixtx_pipe_get_config_t getCurrentArgs   = { 0 };
    ctl_pixtx_block_config_t    lutConfig        = pPixelConfigCaps->pBlockConfigs[oneDLUTIndex];

    lutConfig.Size                               = sizeof(ctl_pixtx_block_config_t);
    getCurrentArgs.Size                          = sizeof(ctl_pixtx_pipe_get_config_t);
    getCurrentArgs.QueryType                     = CTL_PIXTX_CONFIG_QUERY_TYPE_CURRENT;
    getCurrentArgs.NumBlocks                     = 1; // Query only one block
    getCurrentArgs.pBlockConfigs                 = &lutConfig;
    lutConfig.Config.OneDLutConfig.pSampleValues = (double *)malloc(CTL_MAX_NUM_SAMPLES_PER_CHANNEL_1D_LUT * lutConfig.Config.OneDLutConfig.NumChannels * sizeof(double));

    NULL_PTR_CHECK(lutConfig.Config.OneDLutConfig.pSampleValues);

    memset(lutConfig.Config.OneDLutConfig.pSampleValues, 0, CTL_MAX_NUM_SAMPLES_PER_CHANNEL_1D_LUT * lutConfig.Config.OneDLutConfig.NumChannels * sizeof(double));

    VERIFY_API_STATUS(ControlApiPixelTransformationGetConfig(hDisplayOutput, &getCurrentArgs));

    DEBUG_LOG("ControlApiPixelTransformationGetConfig for Query Current Passed\n");

    lutDataSize = lutConfig.Config.OneDLutConfig.NumSamplesPerChannel * lutConfig.Config.OneDLutConfig.NumChannels;
    DEBUG_LOG("LutDataSize = %d\n ", lutDataSize);

    DEBUG_LOG("Gamma values : pSampleValues\n");
    for (sampleValueIndex = 0; sampleValueIndex < lutDataSize; sampleValueIndex++)
    {
        DEBUG_LOG("LutConfig.Config.OneDLutConfig.pSampleValues[%d] = %f\n", sampleValueIndex, lutConfig.Config.OneDLutConfig.pSampleValues[sampleValueIndex]);
    }
    memcpy_s(argsLutConfig, sizeof(ctl_pixtx_block_config_t), &lutConfig, sizeof(ctl_pixtx_block_config_t));

    for (uint32_t SampleValueIndex = 0; SampleValueIndex < lutDataSize; SampleValueIndex++)
    {
        DEBUG_LOG("LutConfig.Config.OneDLutConfig.pSampleValues[%d] = %f\n", SampleValueIndex, argsLutConfig->Config.OneDLutConfig.pSampleValues[SampleValueIndex]);
    }

    FREE_MEMORY(lutConfig.Config.OneDLutConfig.pSampleValues);

    return apiResult;
}

bool ControlAPIGetGamma(ctl_pixtx_pipe_get_config_t *argsGetConfig, ctl_pixtx_block_config_t *argsLutConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetGamma !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during GetGamma Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetGamma: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks - %d\n", pixelConfigCaps.NumBlocks);

                const uint32_t blocksToQuery = pixelConfigCaps.NumBlocks;

                // Allocate required memory as per number of blocks supported.
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for BlockType : 0x%X\n", apiResult);
                        goto END;
                    }

                    // Iterate through blocks pixelConfigCaps and find the 1DLUT block index.
                    int32_t oneDLUTIndex = -1;

                    for (uint32_t i = 0; i < pixelConfigCaps.NumBlocks; i++)
                    {
                        if (CTL_PIXTX_BLOCK_TYPE_1D_LUT == pixelConfigCaps.pBlockConfigs[i].BlockType)
                        {
                            oneDLUTIndex = i;
                            break;
                        }
                    }
                    if (oneDLUTIndex < 0)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig: No 1DLUT Block Capability\n");
                    }

                    apiResult = GetGamma(hDisplayActive[displayIndex], &pixelConfigCaps, oneDLUTIndex, argsLutConfig);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("GetGamma call Failed\n");
                    }
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool SetGamma(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pPixelConfigCaps, int32_t oneDLUTIndex, double *blockConfig)
{
    bool                        apiResult                = TRUE;
    ctl_pixtx_pipe_set_config_t setGammaArgs             = { 0 };
    ctl_pixtx_block_config_t    lutBlockConfig           = pPixelConfigCaps->pBlockConfigs[oneDLUTIndex];
    lutBlockConfig.Size                                  = sizeof(ctl_pixtx_block_config_t);
    lutBlockConfig.Config.OneDLutConfig.SamplingType     = CTL_PIXTX_LUT_SAMPLING_TYPE_UNIFORM;
    lutBlockConfig.Config.OneDLutConfig.NumChannels      = 3;
    lutBlockConfig.Config.OneDLutConfig.pSamplePositions = NULL;

    const uint32_t lutSize                            = lutBlockConfig.Config.OneDLutConfig.NumSamplesPerChannel * lutBlockConfig.Config.OneDLutConfig.NumChannels;
    lutBlockConfig.Config.OneDLutConfig.pSampleValues = (double *)malloc(lutSize * sizeof(double));

    NULL_PTR_CHECK(lutBlockConfig.Config.OneDLutConfig.pSampleValues);

    /* TODO: Check and remove
    memcpy_s(lutBlockConfig.Config.OneDLutConfig.pSampleValues, sizeof(lutBlockConfig.Config.OneDLutConfig.pSampleValues), blockConfig->Config.OneDLutConfig.pSampleValues,
             sizeof(blockConfig->Config.OneDLutConfig.pSampleValues));
    */

    for (uint32_t index = 0; index < (lutSize / lutBlockConfig.Config.OneDLutConfig.NumChannels); index++)
    {
        lutBlockConfig.Config.OneDLutConfig.pSampleValues[3 * index]     = lutBlockConfig.Config.OneDLutConfig.pSampleValues[3 * index + 1] =
        lutBlockConfig.Config.OneDLutConfig.pSampleValues[3 * index + 2] = blockConfig[index];
    }

    DEBUG_LOG("Lut Sample Values to be Set\n");
    for (uint32_t valueIndex = 0; valueIndex < lutSize; valueIndex++)
    {
        DEBUG_LOG("pSampleValues[%d] = %f\n", valueIndex, lutBlockConfig.Config.OneDLutConfig.pSampleValues[valueIndex]);
    }

    setGammaArgs.Size          = sizeof(ctl_pixtx_pipe_set_config_t);
    setGammaArgs.OpertaionType = CTL_PIXTX_CONFIG_OPERTAION_TYPE_SET_CUSTOM;
    setGammaArgs.NumBlocks     = 1;
    setGammaArgs.pBlockConfigs = &lutBlockConfig;

    apiResult = ControlApiPixelTransformationSetConfig(hDisplayOutput, &setGammaArgs);
    if (apiResult != TRUE)
    {
        ERROR_LOG("ControlApiPixelTransformationSetConfig for SetGamma Failed: 0x%X\n", apiResult);
        FREE_MEMORY(lutBlockConfig.Config.OneDLutConfig.pSampleValues);
        return apiResult;
    }

    DEBUG_LOG("ControlApiPixelTransformationSetConfig for SetGamma Passed\n");
    FREE_MEMORY(lutBlockConfig.Config.OneDLutConfig.pSampleValues);

    return apiResult;
}

bool ControlAPISetGamma(ctl_pixtx_pipe_set_config_t *argsSetConfig, double *blockConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    uint32_t                     blockIndex      = 0;
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    NULL_PTR_CHECK(argsSetConfig);
    NULL_PTR_CHECK(blockConfig);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetGamma !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during SetGamma Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPISetGamma: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks - %d\n", pixelConfigCaps.NumBlocks);

                const uint32_t blocksToQuery = pixelConfigCaps.NumBlocks;

                // Allocate required memory as per number of blocks supported.
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for BlockType : 0x%X\n", apiResult);
                        goto END;
                    }
                    DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for BlockType\n");
                    // Iterate through blocks pixelConfigCaps and find the 1DLUT block index.
                    int32_t oneDLUTIndex = -1;

                    for (blockIndex = 0; blockIndex < pixelConfigCaps.NumBlocks; blockIndex++)
                    {
                        if (CTL_PIXTX_BLOCK_TYPE_1D_LUT == pixelConfigCaps.pBlockConfigs[blockIndex].BlockType)
                        {
                            oneDLUTIndex = blockIndex;
                            break;
                        }
                    }
                    if (oneDLUTIndex < 0)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig: No 1DLUT Block Capability\n");
                    }

                    apiResult = SetGamma(hDisplayActive[displayIndex], &pixelConfigCaps, oneDLUTIndex, blockConfig);
                    if (TRUE != apiResult)
                    {
                        ERROR_LOG("SetGamma call Failed\n");
                    }
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool SetCSC(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pPixelConfigCaps, int32_t cscBlockIndex, ctl_pixtx_pipe_set_config_t *argsCSC,
            ctl_pixtx_block_config_t *blockConfig)
{
    bool                        apiResult  = TRUE;
    ctl_pixtx_pipe_set_config_t setCSCArgs = { 0 };
    ctl_pixtx_block_config_t    cscConfig  = pPixelConfigCaps->pBlockConfigs[cscBlockIndex];
    cscConfig.BlockType                    = blockConfig->BlockType;
    cscConfig.Size                         = blockConfig->Size;

    for (uint32_t preIndex = 0; preIndex < 3; preIndex++)
    {
        cscConfig.Config.MatrixConfig.PreOffsets[preIndex] = blockConfig->Config.MatrixConfig.PreOffsets[preIndex];
    }
    for (uint32_t posIndex = 0; posIndex < 3; posIndex++)
    {
        cscConfig.Config.MatrixConfig.PostOffsets[posIndex] = blockConfig->Config.MatrixConfig.PostOffsets[posIndex];
    }

    memcpy_s(cscConfig.Config.MatrixConfig.Matrix, sizeof(cscConfig.Config.MatrixConfig.Matrix), blockConfig->Config.MatrixConfig.Matrix,
             sizeof(blockConfig->Config.MatrixConfig.Matrix));

    setCSCArgs.Size                     = argsCSC->Size;
    setCSCArgs.OpertaionType            = argsCSC->OpertaionType;
    setCSCArgs.NumBlocks                = 1; // Set only one block for CSC
    setCSCArgs.pBlockConfigs            = &cscConfig;
    setCSCArgs.pBlockConfigs->BlockId   = pPixelConfigCaps->pBlockConfigs[cscBlockIndex].BlockId;
    setCSCArgs.pBlockConfigs->BlockType = blockConfig->BlockType;

    apiResult = ControlApiPixelTransformationSetConfig(hDisplayOutput, &setCSCArgs);

    return apiResult;
}

bool ControlAPISetCSC(ctl_pixtx_pipe_set_config_t *argsSetCSC, ctl_pixtx_block_config_t *blockConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    NULL_PTR_CHECK(blockConfig);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetCSC !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during SetCSC Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPISetCSC: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks - %d\n", pixelConfigCaps.NumBlocks);

                // Allocate required memory based on number of blocks supported.
                const uint32_t blocksToQuery  = pixelConfigCaps.NumBlocks;
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig for Query type Capability Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    // Iterate through blocks pixelConfigCaps and find the CSC block index.
                    int32_t cscBlock = -1;

                    for (uint32_t blockIndex = 0; blockIndex < pixelConfigCaps.NumBlocks; blockIndex++)
                    {
                        if (CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX == pixelConfigCaps.pBlockConfigs[blockIndex].BlockType)
                        {
                            cscBlock = blockIndex;
                            break;
                        }
                    }
                    if (cscBlock < 0)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig: No CSC Block Capability\n");
                    }

                    apiResult = SetCSC(hDisplayActive[displayIndex], &pixelConfigCaps, cscBlock, argsSetCSC, blockConfig);
                    if (TRUE != apiResult)
                    {
                        ERROR_LOG("SetCSC call Failed 0x%X\n", apiResult);
                    }
                    DEBUG_LOG("ControlApiPixelTransformationSetConfig for SetCSC Matrix Passed\n");
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

void FetchColorBlockIndex(ctl_pixtx_pipe_get_config_t *blkConfig, int32_t *HW3DLUTIndex, int32_t *DGLUTIndex, int32_t *CSCIndex, int32_t *GLUTIndex, int32_t *oCSCIndex,
                          uint8_t enabledMode)
{
    uint32_t OneDLutOccurances = 0;

    for (uint32_t i = 0; i < blkConfig->NumBlocks; i++)
    {
        if (CTL_PIXTX_BLOCK_TYPE_1D_LUT == blkConfig->pBlockConfigs[i].BlockType)
        {
            DEBUG_LOG("Enabled Mode is %d\n", enabledMode);
            // In HDR Mode, the DGLUT block's support would be updated as False, hence the Block Index of GLUT will change
            if ((enabledMode == HDR) || (enabledMode == WCG))
            {
                *GLUTIndex = i;
                OneDLutOccurances++;
            }
            else
            {
                if (OneDLutOccurances == 0)
                {
                    *DGLUTIndex = i;
                }
                else if (OneDLutOccurances == 1)
                {
                    *GLUTIndex = i;
                }
                OneDLutOccurances++;
            }
        }
        else if ((CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX_AND_OFFSETS == blkConfig->pBlockConfigs[i].BlockType))
        {
            *CSCIndex = i;
        }

        else if ((CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX == blkConfig->pBlockConfigs[i].BlockType))
        {
            *oCSCIndex = i;
        }

        else if ((CTL_PIXTX_BLOCK_TYPE_3D_LUT == blkConfig->pBlockConfigs[i].BlockType))
        {
            *HW3DLUTIndex = i;
        }
    }
}

void FillDataForCSC(uint32_t BlkIndex, ctl_pixtx_pipe_set_config_t *SetPixTxArgs, ctl_pixtx_block_config_t *CSCConfig)
{

    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockId   = CSCConfig->BlockId;
    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockType = CSCConfig->BlockType;

    memcpy_s(SetPixTxArgs->pBlockConfigs[BlkIndex].Config.MatrixConfig.Matrix, sizeof(SetPixTxArgs->pBlockConfigs[BlkIndex].Config.MatrixConfig.Matrix),
             CSCConfig->Config.MatrixConfig.Matrix, sizeof(CSCConfig->Config.MatrixConfig.Matrix));
}

void FillDataForDGLUT(uint32_t BlkIndex, ctl_pixtx_pipe_set_config_t *SetPixTxArgs, ctl_pixtx_block_config_t *DGLUTConfig)
{
    const uint32_t DGLutSize                                               = DGLUTConfig->Config.OneDLutConfig.NumSamplesPerChannel * DGLUTConfig->Config.OneDLutConfig.NumChannels;
    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockId                          = DGLUTConfig->BlockId;
    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockType                        = DGLUTConfig->BlockType;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumChannels = DGLUTConfig->Config.OneDLutConfig.NumChannels;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumSamplesPerChannel = DGLUTConfig->Config.OneDLutConfig.NumSamplesPerChannel;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.SamplingType         = DGLUTConfig->Config.OneDLutConfig.SamplingType;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.pSampleValues        = (double *)malloc(DGLutSize * sizeof(double));

    for (uint32_t dindex = 0; dindex < DGLutSize; dindex++)
    {
        SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.pSampleValues[dindex] = DGLUTConfig->Config.OneDLutConfig.pSampleValues[dindex];
    }
}

void FillDataForGLUT(uint32_t BlkIndex, ctl_pixtx_pipe_set_config_t *SetPixTxArgs, ctl_pixtx_block_config_t *GLUTConfig)
{
    const uint32_t GLutSize                                                = GLUTConfig->Config.OneDLutConfig.NumSamplesPerChannel * GLUTConfig->Config.OneDLutConfig.NumChannels;
    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockId                          = GLUTConfig->BlockId;
    SetPixTxArgs->pBlockConfigs[BlkIndex].BlockType                        = GLUTConfig->BlockType;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumChannels = GLUTConfig->Config.OneDLutConfig.NumChannels;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumSamplesPerChannel = GLUTConfig->Config.OneDLutConfig.NumSamplesPerChannel;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.SamplingType         = GLUTConfig->Config.OneDLutConfig.SamplingType;
    SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.pSampleValues        = (double *)malloc(GLutSize * sizeof(double));

    double *pRedLut   = SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.pSampleValues;
    double *pGreenLut = pRedLut + SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumSamplesPerChannel;
    double *pBlueLut  = pGreenLut + SetPixTxArgs->pBlockConfigs[BlkIndex].Config.OneDLutConfig.NumSamplesPerChannel;

    for (uint32_t index = 0; index < GLUTConfig->Config.OneDLutConfig.NumSamplesPerChannel; index++)
    {
        pRedLut[index] = pGreenLut[index] = pBlueLut[index] = GLUTConfig->Config.OneDLutConfig.pSampleValues[index];
    }
}

bool ControlAPISetColorFeature(ctl_pixtx_pipe_set_config_t *argsSetColorBlks, ctl_pixtx_pipe_get_config_t *blkConfig, PANEL_INFO *pPanelInfo, uint32_t user_req_blk,
                               uint8_t Enabled_Mode)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);
    ctl_pixtx_pipe_set_config_t SetPixTxArgs     = { 0 };
    int32_t                     HW3DLUTIndex = -1, DGLUTIndex = -1, CscIndex = -1, GLUTIndex = -1, oCSCIndex = -1;

    DEBUG_LOG("USER REQUESTED BLOCK %d\n", user_req_blk);

    NULL_PTR_CHECK(argsSetColorBlks);
    NULL_PTR_CHECK(blkConfig);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetFeature !!!");
        goto END;
    }

    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during SetCSC Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }
            }

            FetchColorBlockIndex(blkConfig, &HW3DLUTIndex, &DGLUTIndex, &CscIndex, &GLUTIndex, &oCSCIndex, Enabled_Mode);

            ctl_pixtx_block_config_t HW3DLUTConfig = blkConfig->pBlockConfigs[HW3DLUTIndex];
            ctl_pixtx_block_config_t DGLUTConfig   = blkConfig->pBlockConfigs[DGLUTIndex];
            ctl_pixtx_block_config_t CSCConfig     = blkConfig->pBlockConfigs[CscIndex];
            ctl_pixtx_block_config_t GLUTConfig    = blkConfig->pBlockConfigs[GLUTIndex];
            ctl_pixtx_block_config_t oCSCConfig    = blkConfig->pBlockConfigs[oCSCIndex];

            SetPixTxArgs.Size          = sizeof(ctl_pixtx_pipe_set_config_t);
            SetPixTxArgs.OpertaionType = CTL_PIXTX_CONFIG_OPERTAION_TYPE_SET_CUSTOM;
            SetPixTxArgs.NumBlocks     = argsSetColorBlks->NumBlocks;
            SetPixTxArgs.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(SetPixTxArgs.NumBlocks * sizeof(ctl_pixtx_block_config_t));

            // If the User Requested Block is only DGLUT
            if (user_req_blk == DGLUT)
                FillDataForDGLUT(0, &SetPixTxArgs, &DGLUTConfig);

            // If the User Requested Block is only Linear CSC
            if (user_req_blk == CSC)
                FillDataForCSC(0, &SetPixTxArgs, &CSCConfig);

            // If the User Requested Block is only GLUT
            if (user_req_blk == GLUT)
                FillDataForGLUT(0, &SetPixTxArgs, &GLUTConfig);

            // If the User Requested Block is only NonLinear CSC
            if (user_req_blk == OCSC)
                FillDataForCSC(0, &SetPixTxArgs, &oCSCConfig);

            // If the User Requested Block is DGLUT and Linear CSC
            if (user_req_blk == DGLUT_CSC)
            {
                FillDataForDGLUT(0, &SetPixTxArgs, &DGLUTConfig);
                FillDataForCSC(1, &SetPixTxArgs, &CSCConfig);
            }

            // If the User Requested Block is DGLUT, Linear CSC and GLUT
            if (user_req_blk == DGLUT_CSC_GLUT)
            {
                FillDataForDGLUT(0, &SetPixTxArgs, &DGLUTConfig);
                FillDataForCSC(1, &SetPixTxArgs, &CSCConfig);
                FillDataForGLUT(2, &SetPixTxArgs, &GLUTConfig);
            }

            // If the user requests for only DGLUT and GLUT Blocks
            if (user_req_blk == DGLUT_GLUT)
            {
                FillDataForDGLUT(0, &SetPixTxArgs, &DGLUTConfig);
                FillDataForGLUT(1, &SetPixTxArgs, &GLUTConfig);
            }

            // If the user requests all the five blocks - HW3DLUT - DGLUT - CSC - GLUT and oCSC
            if (user_req_blk == ALL)
            {
                FillDataForDGLUT(0, &SetPixTxArgs, &DGLUTConfig); // For Degamma LUT
                FillDataForCSC(1, &SetPixTxArgs, &CSCConfig);     // For Pipe CSC
                FillDataForGLUT(2, &SetPixTxArgs, &GLUTConfig);   // For Gamma LUT
                FillDataForCSC(1, &SetPixTxArgs, &CSCConfig);     // For oCSC
            }

            apiResult = ControlApiPixelTransformationSetConfig(hDisplayActive[displayIndex], &SetPixTxArgs);
            if (TRUE != apiResult)
            {
                ERROR_LOG("SetFeature call Failed 0x%X\n", apiResult);
                goto END;
            }
            FREE_MEMORY(SetPixTxArgs.pBlockConfigs);
            return TRUE;
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool RestoreDefault(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pixelConfigCaps)
{
    bool                        apiResult             = TRUE;
    ctl_pixtx_pipe_set_config_t setRestoreDefaultArgs = { 0 };
    setRestoreDefaultArgs.Size                        = sizeof(ctl_pixtx_pipe_set_config_t);
    setRestoreDefaultArgs.OpertaionType               = CTL_PIXTX_CONFIG_OPERTAION_TYPE_RESTORE_DEFAULT;
    setRestoreDefaultArgs.NumBlocks                   = pixelConfigCaps->NumBlocks;
    setRestoreDefaultArgs.pBlockConfigs               = pixelConfigCaps->pBlockConfigs;

    apiResult = ControlApiPixelTransformationSetConfig(hDisplayOutput, &setRestoreDefaultArgs);

    return apiResult;
}

bool ControlAPIRestoreDefault(ctl_pixtx_pipe_set_config_t *argsRestoreDefault, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIRestoreDefault !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during Restore Default Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIRestoreDefault: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Number of Blocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks -%d\n", pixelConfigCaps.NumBlocks);

                // Allocate required memory based on number of blocks supported.
                const uint32_t blocksToQuery  = pixelConfigCaps.NumBlocks;
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed: 0x%X\n", apiResult);
                        goto END;
                    }

                    // Restore Default
                    apiResult = RestoreDefault(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (TRUE != apiResult)
                    {
                        ERROR_LOG("RestoreDefault call Failed\n");
                    }
                    INFO_LOG("ControlApiPixelTransformationSetConfig for Restore Default Passed\n");
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

void MatrixMult3x3(double matrixA[3][3], double matrixB[3][3], double resultMatrix[3][3])
{
    double intermediateMatrix[3][3] = { 0 };

    for (uint8_t col = 0; col < 3; col++)
    {
        for (uint8_t row = 0; row < 3; row++)
        {
            intermediateMatrix[col][row] = matrixA[col][0] * matrixB[0][row] + matrixA[col][1] * matrixB[1][row] + matrixA[col][2] * matrixB[2][row];
        }
    }

    for (uint8_t coly = 0; coly < 3; coly++)
    {
        for (uint8_t rowx = 0; rowx < 3; rowx++)
        {
            resultMatrix[coly][rowx] = intermediateMatrix[coly][rowx];
        }
    }
}

void GenerateHueSaturationMatrix(double Hue, double Saturation, double CoEff[3][3])
{
    double HueShift = (double)Hue * 0.01745329252; // Pi / 180 = 0.01745329252
    double SatShift = (double)Saturation;
    double C        = cos(HueShift);
    double S        = sin(HueShift);
    double ResultMatrix[3][3];

    double HueRotationMatrix[3][3]           = { { 1.0, 0.0, 0.0 }, { 0.0, C, -S }, { 0.0, S, C } };
    double Sat                               = 1.0 + (SatShift / 100);
    double SaturationEnhancementMatrix[3][3] = { { 1.0, 0.0, 0.0 }, { 0.0, Sat, 0.0 }, { 0.0, 0.0, Sat } };

    // Use Bt.709 coefficients for RGB and YCbCr709
    MatrixMult3x3(YCbCr2RGB709, SaturationEnhancementMatrix, ResultMatrix);
    MatrixMult3x3(ResultMatrix, HueRotationMatrix, ResultMatrix);
    MatrixMult3x3(ResultMatrix, RGB2YCbCr709, ResultMatrix);

    // Copy resultant matrix
    memcpy_s(CoEff, sizeof(ResultMatrix), ResultMatrix, sizeof(ResultMatrix));
}

bool ApplyHueSaturation(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_get_config_t *pPixelConfigCaps, int32_t cscBlockIndex, double Hue, double Saturation,
                        ctl_pixtx_pipe_set_config_t *argsCSC, ctl_pixtx_block_config_t *blockConfig)
{
    bool                        apiResult  = TRUE;
    ctl_pixtx_pipe_set_config_t setCSCArgs = { 0 };
    ctl_pixtx_block_config_t    cscConfig  = pPixelConfigCaps->pBlockConfigs[cscBlockIndex];
    cscConfig.BlockType                    = blockConfig->BlockType;
    cscConfig.Size                         = blockConfig->Size;

    if ((0 == Hue || 360 == Hue) && (0 == Saturation))
    {
        // For Default Hue & Sat values, CSC Cofficients should be Identity Matrix
        memset(cscConfig.Config.MatrixConfig.Matrix, 0, sizeof(cscConfig.Config.MatrixConfig.Matrix));
        memcpy_s(cscConfig.Config.MatrixConfig.Matrix, sizeof(cscConfig.Config.MatrixConfig.Matrix), blockConfig->Config.MatrixConfig.Matrix,
                 sizeof(blockConfig->Config.MatrixConfig.Matrix));
    }
    else
    {
        // Generate Non Linear CSC Matrix for Hue, Saturation values.
        GenerateHueSaturationMatrix(Hue, Saturation, cscConfig.Config.MatrixConfig.Matrix);
    }

    setCSCArgs.Size                   = argsCSC->Size;
    setCSCArgs.OpertaionType          = argsCSC->OpertaionType;
    setCSCArgs.NumBlocks              = 1;
    setCSCArgs.pBlockConfigs          = &cscConfig;
    setCSCArgs.pBlockConfigs->BlockId = pPixelConfigCaps->pBlockConfigs[cscBlockIndex].BlockId;

    apiResult = ControlApiPixelTransformationSetConfig(hDisplayOutput, &setCSCArgs);
    return apiResult;
}

bool ControlAPIHueSaturation(ctl_pixtx_pipe_set_config_t *argsSetCSC, ctl_pixtx_block_config_t *blockConfig, double hueValue, double satValue, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    NULL_PTR_CHECK(blockConfig);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIHueSaturation !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during HueSaturation Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIHueSaturation: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks - %d\n", pixelConfigCaps.NumBlocks);

                // Allocate required memory based on number of blocks supported.
                const uint32_t blocksToQuery  = pixelConfigCaps.NumBlocks;
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig for Query type Capability Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    // Iterate through blocks pixelConfigCaps and find the CSC block index.
                    int32_t cscBlock = -1;

                    for (uint32_t blockIndex = 0; blockIndex < pixelConfigCaps.NumBlocks; blockIndex++)
                    {
                        if (CTL_PIXTX_BLOCK_TYPE_3X3_MATRIX == pixelConfigCaps.pBlockConfigs[blockIndex].BlockType)
                        {
                            cscBlock = blockIndex;
                            break;
                        }
                    }
                    if (cscBlock < 0)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig: No CSC Block Capability\n");
                    }

                    apiResult = ApplyHueSaturation(hDisplayActive[displayIndex], &pixelConfigCaps, cscBlock, hueValue, satValue, argsSetCSC, blockConfig);
                    if (TRUE != apiResult)
                    {
                        ERROR_LOG("HueSaturation call Failed 0x%X\n", apiResult);
                    }
                    DEBUG_LOG("ControlApiPixelTransformationSetConfig for HueSaturation Matrix Passed\n");
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool Set3DLut(ctl_display_output_handle_t hDisplayOutput, ctl_pixtx_pipe_set_config_t *pPixelConfigCaps, int32_t threeDLUTIndex, ctl_pixtx_block_config_t *blockConfig)
{
    bool                        apiResult      = TRUE;
    ctl_pixtx_pipe_set_config_t setArgs        = { 0 };
    ctl_pixtx_block_config_t    lutBlockConfig = pPixelConfigCaps->pBlockConfigs[threeDLUTIndex];
    lutBlockConfig.Size                        = sizeof(ctl_pixtx_block_config_t);

    // Create a valid 3D LUT.
    uint8_t lutDepth = lutBlockConfig.Config.ThreeDLutConfig.NumSamplesPerChannel;

    const uint32_t lutSize                              = lutDepth * lutDepth * lutDepth;
    lutBlockConfig.Config.ThreeDLutConfig.pSampleValues = (ctl_pixtx_3dlut_sample_t *)malloc(lutSize * sizeof(ctl_pixtx_3dlut_sample_t));
    NULL_PTR_CHECK(lutBlockConfig.Config.ThreeDLutConfig.pSampleValues);
    memset(lutBlockConfig.Config.ThreeDLutConfig.pSampleValues, 0, lutSize * sizeof(ctl_pixtx_3dlut_sample_t));

    DEBUG_LOG("pSampleValues which has to set are as below\n");
    for (uint32_t valueIndex = 0; valueIndex < lutSize; valueIndex++)
    {
        DEBUG_LOG(" Red   pSampleValues[%d] = %f\n", valueIndex, blockConfig->Config.ThreeDLutConfig.pSampleValues[valueIndex].Red);
        DEBUG_LOG(" Green pSampleValues[%d] = %f\n", valueIndex, blockConfig->Config.ThreeDLutConfig.pSampleValues[valueIndex].Green);
        DEBUG_LOG(" Blue  pSampleValues[%d] = %f\n", valueIndex, blockConfig->Config.ThreeDLutConfig.pSampleValues[valueIndex].Blue);
    }

    setArgs.Size          = sizeof(ctl_pixtx_pipe_set_config_t);
    setArgs.OpertaionType = CTL_PIXTX_CONFIG_OPERTAION_TYPE_SET_CUSTOM;
    setArgs.NumBlocks     = 1;
    setArgs.pBlockConfigs = blockConfig;
    setArgs.Flags         = CTL_PIXTX_PIPE_SET_CONFIG_FLAG_PERSIST_ACROSS_POWER_EVENTS;

    apiResult = ControlApiPixelTransformationSetConfig(hDisplayOutput, &setArgs);
    if (TRUE != apiResult)
    {
        ERROR_LOG("ControlApiPixelTransformationSetConfig for Set 3DLUT Failed: 0x%X\n", apiResult);
        FREE_MEMORY(lutBlockConfig.Config.ThreeDLutConfig.pSampleValues);
        return apiResult;
    }
    DEBUG_LOG("ControlApiPixelTransformationSetConfig for Set 3DLUT Passed\n");

    FREE_MEMORY(lutBlockConfig.Config.ThreeDLutConfig.pSampleValues);
    return apiResult;
}

bool ControlAPISet3DLUT(ctl_pixtx_pipe_set_config_t *argsSetConfig, ctl_pixtx_block_config_t *blockConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_pixtx_pipe_get_config_t  pixelConfigCaps = { 0 };
    uint32_t                     blockIndex      = 0;
    pixelConfigCaps.QueryType                    = CTL_PIXTX_CONFIG_QUERY_TYPE_CAPABILITY;
    pixelConfigCaps.Size                         = sizeof(ctl_pixtx_pipe_get_config_t);

    NULL_PTR_CHECK(argsSetConfig);
    // NULL_PTR_CHECK(blockConfig);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISet3DLUT !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during Set3DLUT Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPISet3DLUT: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for NumBlocks: 0x%X\n", apiResult);
                    goto END;
                }

                if (0 == pixelConfigCaps.NumBlocks)
                {
                    ERROR_LOG("ControlApiPixelTransformationGetConfig NumBlocks is zero (Invalid Size)\n");
                    goto END;
                }
                DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for NumBlocks - %d\n", pixelConfigCaps.NumBlocks);

                const uint32_t blocksToQuery = pixelConfigCaps.NumBlocks;

                // Allocate required memory as per number of blocks supported.
                pixelConfigCaps.pBlockConfigs = (ctl_pixtx_block_config_t *)malloc(blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                if (NULL != pixelConfigCaps.pBlockConfigs)
                {
                    memset(pixelConfigCaps.pBlockConfigs, 0, blocksToQuery * sizeof(ctl_pixtx_block_config_t));

                    apiResult = ControlApiPixelTransformationGetConfig(hDisplayActive[displayIndex], &pixelConfigCaps);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig Query Capability Failed for BlockType : 0x%X\n", apiResult);
                        goto END;
                    }
                    DEBUG_LOG("ControlApiPixelTransformationGetConfig Query Capability Passed for BlockType\n");
                    // Iterate through blocks pixelConfigCaps and find the 3DLUT block index.
                    int32_t threeDLUTIndex = -1;

                    for (blockIndex = 0; blockIndex < pixelConfigCaps.NumBlocks; blockIndex++)
                    {
                        if (CTL_PIXTX_BLOCK_TYPE_3D_LUT == pixelConfigCaps.pBlockConfigs[blockIndex].BlockType)
                        {
                            threeDLUTIndex = blockIndex;
                            break;
                        }
                    }
                    if (threeDLUTIndex < 0)
                    {
                        ERROR_LOG("ControlApiPixelTransformationGetConfig: No 3DLUT Block Capability\n");
                    }

                    apiResult = Set3DLut(hDisplayActive[displayIndex], argsSetConfig, threeDLUTIndex, blockConfig);
                    if (TRUE != apiResult)
                    {
                        ERROR_LOG("Set3DLut call Failed\n");
                    }
                }
                FREE_MEMORY(pixelConfigCaps.pBlockConfigs);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetDPST(ctl_power_optimization_settings_t *argsSetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t setPowerSettings = { 0 };
    ctl_power_optimization_settings_t disablePSR       = { 0 };
    ctl_power_optimization_settings_t getPowerSettings = { 0 };
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;

    NULL_PTR_CHECK(argsSetPowerSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetDPST !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!\n");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPISetDPST: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getPowerCaps.Size = sizeof(ctl_power_optimization_caps_t);
                apiResult         = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps call failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetPowerOptimizationCaps Query Passed\n");

                if (TRUE == apiResult && (getPowerCaps.SupportedFeatures & CTL_POWER_OPTIMIZATION_FLAG_DPST))
                {
                    DEBUG_LOG("PowerOptimizationFeature %d, EnabledFeatures %d, Enable %d, PowerSource %d, PowerOptimizationPlan %d, Level %d  \n",
                              argsSetPowerSettings->PowerOptimizationFeature, argsSetPowerSettings->FeatureSpecificData.DPSTInfo.EnabledFeatures, argsSetPowerSettings->Enable,
                              argsSetPowerSettings->PowerSource, argsSetPowerSettings->PowerOptimizationPlan, argsSetPowerSettings->FeatureSpecificData.DPSTInfo.Level);
                    setPowerSettings.PowerOptimizationFeature                     = CTL_POWER_OPTIMIZATION_FLAG_DPST;
                    setPowerSettings.FeatureSpecificData.DPSTInfo.EnabledFeatures = argsSetPowerSettings->FeatureSpecificData.DPSTInfo.EnabledFeatures;
                    setPowerSettings.Size                                         = sizeof(ctl_power_optimization_settings_t);
                    setPowerSettings.Enable                                       = argsSetPowerSettings->Enable;
                    setPowerSettings.PowerSource                                  = argsSetPowerSettings->PowerSource;
                    setPowerSettings.PowerOptimizationPlan                        = argsSetPowerSettings->PowerOptimizationPlan;
                    setPowerSettings.FeatureSpecificData.DPSTInfo.Level           = argsSetPowerSettings->FeatureSpecificData.DPSTInfo.Level;
                    apiResult                                                     = ControlApiSetPowerOptimizationSetting(hDisplayActive[displayIndex], &setPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiSetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    DEBUG_LOG("ControlApiSetPowerOptimizationSetting for DPST Passed\n");
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetDPST(ctl_power_optimization_settings_t *argsGetPowerSettings, PANEL_INFO *pPanelInfo)
{
    bool                              apiResult        = TRUE;
    uint32_t                          adapterIndex     = 0;
    uint32_t                          adapterCount     = 0;
    uint32_t                          displayCount     = 0;
    uint32_t                          displayIndex     = 0;
    ctl_device_adapter_handle_t *     hDevices         = nullptr;
    ctl_device_adapter_handle_t *     hActDevices      = nullptr;
    ctl_display_output_handle_t *     hDisplayOutput   = nullptr;
    ctl_display_output_handle_t *     hDisplayActive   = nullptr;
    ctl_power_optimization_caps_t     getPowerCaps     = { 0 };
    ctl_power_optimization_settings_t getPowerSettings = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetDPST !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }
        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetDPST: displayCount %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getPowerCaps.Size = sizeof(ctl_power_optimization_caps_t);
                apiResult         = ControlApiGetPowerOptimizationCaps(hDisplayActive[displayIndex], &getPowerCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetPowerOptimizationCaps Call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetPowerOptimizationCaps Query Call Passed\n");

                if (TRUE == apiResult && (getPowerCaps.SupportedFeatures & CTL_POWER_OPTIMIZATION_FLAG_DPST))
                {
                    getPowerSettings.Size                     = sizeof(ctl_power_optimization_settings_t);
                    getPowerSettings.PowerOptimizationFeature = CTL_POWER_OPTIMIZATION_FLAG_DPST;
                    getPowerSettings.PowerSource              = argsGetPowerSettings->PowerSource;
                    getPowerSettings.PowerOptimizationPlan    = argsGetPowerSettings->PowerOptimizationPlan;
                    apiResult                                 = ControlApiGetPowerOptimizationSetting(hDisplayActive[displayIndex], &getPowerSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiGetPowerOptimizationSetting Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }
                    memcpy_s(argsGetPowerSettings, sizeof(ctl_power_optimization_settings_t), &getPowerSettings, sizeof(ctl_power_optimization_settings_t));

                    DEBUG_LOG("ControlApiGetPowerOptimizationSetting Call Passed\n");
                    DEBUG_LOG("DPST GetPowerSettings.Enable = %d\n", getPowerSettings.Enable);
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetScalingCaps(ctl_scaling_caps_t *argsGetScalingCaps, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult            = TRUE;
    bool                         displayAdapterStatus = TRUE;
    uint32_t                     adapterIndex         = 0;
    uint32_t                     adapterCount         = 0;
    uint32_t                     displayCount         = 0;
    uint32_t                     displayIndex         = 0;
    ctl_device_adapter_handle_t *hDevices             = nullptr;
    ctl_device_adapter_handle_t *hActDevices          = nullptr;
    ctl_display_output_handle_t *hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *hDisplayActive       = nullptr;
    ctl_scaling_caps_t           getScalingCaps       = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScalingCaps !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetScaling: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getScalingCaps.Size = sizeof(ctl_scaling_caps_t);
                apiResult           = ControlApiGetSupportedScalingCapability(hDisplayActive[displayIndex], &getScalingCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetSupportedScalingCapability Call Failed : 0x%X\n", apiResult);
                    goto END;
                }
                memcpy_s(argsGetScalingCaps, argsGetScalingCaps->Size, &getScalingCaps, getScalingCaps.Size);
                DEBUG_LOG("ControlApiGetSupportedScalingCapability Query Call Passed\n");
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetRetroScalingCaps(ctl_retro_scaling_caps_t *argsGetScalingCaps, PANEL_INFO *pPanelInfo)
{

    bool                         apiResult            = TRUE;
    bool                         displayAdapterStatus = TRUE;
    uint32_t                     adapterIndex         = 0;
    uint32_t                     adapterCount         = 0;
    uint32_t                     displayCount         = 0;
    uint32_t                     displayIndex         = 0;
    ctl_device_adapter_handle_t *hDevices             = nullptr;
    ctl_device_adapter_handle_t *hActDevices          = nullptr;
    ctl_display_output_handle_t *hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *hDisplayActive       = nullptr;
    ctl_retro_scaling_caps_t     getScalingCaps       = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetRetroScalingCaps !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetRetroScalingCaps: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getScalingCaps.Size = sizeof(ctl_scaling_caps_t);
                apiResult           = ControlApiGetSupportedRetroScalingCapability(hActDevices[displayIndex], &getScalingCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetSupportedRetroScalingCapability Call Failed : 0x%X\n", apiResult);
                    goto END;
                }
                memcpy_s(argsGetScalingCaps, argsGetScalingCaps->Size, &getScalingCaps, getScalingCaps.Size);
                DEBUG_LOG("ControlApiGetSupportedRetroScalingCapability Query Call Passed\n");
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetScaling(ctl_scaling_settings_t *argsGetScalingSettings, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult          = TRUE;
    uint32_t                     adapterIndex       = 0;
    uint32_t                     adapterCount       = 0;
    uint32_t                     displayCount       = 0;
    uint32_t                     displayIndex       = 0;
    ctl_device_adapter_handle_t *hDevices           = nullptr;
    ctl_device_adapter_handle_t *hActDevices        = nullptr;
    ctl_display_output_handle_t *hDisplayOutput     = nullptr;
    ctl_display_output_handle_t *hDisplayActive     = nullptr;
    ctl_scaling_caps_t           getScalingCaps     = { 0 };
    ctl_scaling_settings_t       getScalingSettings = { 0 };

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScaling !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPIGetScaling: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                getScalingCaps.Size = sizeof(ctl_scaling_caps_t);
                apiResult           = ControlApiGetSupportedScalingCapability(hDisplayActive[displayIndex], &getScalingCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetSupportedScalingCapability Call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetSupportedScalingCapability Query Call Passed\n");

                if (TRUE == apiResult && (getScalingCaps.SupportedScaling != 0))
                {
                    getScalingSettings.Size = sizeof(ctl_scaling_settings_t);
                    apiResult               = ControlApiGetCurrentScaling(hDisplayActive[displayIndex], &getScalingSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiGetCurrentScaling Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }
                    memcpy_s(argsGetScalingSettings, argsGetScalingSettings->Size, &getScalingSettings, getScalingSettings.Size);

                    DEBUG_LOG("ControlApiGetCurrentScaling Call Passed\n");
                    DEBUG_LOG("Scaling Enable = %d, ScalingType = %d, PreferredScalingType = %d \n", getScalingSettings.Enable, getScalingSettings.ScalingType,
                              getScalingSettings.PreferredScalingType);
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetScaling(ctl_scaling_settings_t *argsSetScalingSettings, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult          = TRUE;
    uint32_t                     adapterIndex       = 0;
    uint32_t                     adapterCount       = 0;
    uint32_t                     displayCount       = 0;
    uint32_t                     displayIndex       = 0;
    ctl_device_adapter_handle_t *hDevices           = nullptr;
    ctl_device_adapter_handle_t *hActDevices        = nullptr;
    ctl_display_output_handle_t *hDisplayOutput     = nullptr;
    ctl_display_output_handle_t *hDisplayActive     = nullptr;
    ctl_scaling_caps_t           setScalingCaps     = { 0 };
    ctl_scaling_settings_t       setScalingSettings = { 0 };

    NULL_PTR_CHECK(argsSetScalingSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScaling !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays !!!\n");
            goto END;
        }
        DEBUG_LOG("ControlAPISetScaling: Display_Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                setScalingCaps.Size = sizeof(ctl_scaling_caps_t);
                apiResult           = ControlApiGetSupportedScalingCapability(hDisplayActive[displayIndex], &setScalingCaps);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlApiGetSupportedScalingCapability Call Failed : 0x%X\n", apiResult);
                    goto END;
                }

                DEBUG_LOG("ControlApiGetSupportedScalingCapability Query Call Passed\n");

                if (TRUE == apiResult && (setScalingCaps.SupportedScaling != 0) && (argsSetScalingSettings->ScalingType == CTL_SCALING_TYPE_FLAG_CUSTOM))
                {
                    setScalingSettings.Enable          = argsSetScalingSettings->Enable;
                    setScalingSettings.ScalingType     = argsSetScalingSettings->ScalingType;
                    setScalingSettings.Size            = argsSetScalingSettings->Size;
                    setScalingSettings.CustomScalingX  = argsSetScalingSettings->CustomScalingX;
                    setScalingSettings.CustomScalingY  = argsSetScalingSettings->CustomScalingY;
                    setScalingSettings.HardwareModeSet = argsSetScalingSettings->HardwareModeSet;

                    apiResult = ControlApiSetCurrentScaling(hDisplayActive[displayIndex], &setScalingSettings);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("ControlApiSetCurrentScaling Call Failed : 0x%X\n", apiResult);
                        goto END;
                    }

                    DEBUG_LOG("ControlApiSetCurrentScaling Call Passed\n");
                }
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetSetRetoScaling(ctl_retro_scaling_settings_t *argsRetroScalingSettings, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult            = TRUE;
    uint32_t                     adapterIndex         = 0;
    uint32_t                     adapterCount         = 0;
    uint32_t                     displayCount         = 0;
    uint32_t                     displayIndex         = 0;
    ctl_device_adapter_handle_t *hDevices             = nullptr;
    ctl_device_adapter_handle_t *hActDevices          = nullptr;
    ctl_display_output_handle_t *hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *hDisplayActive       = nullptr;
    ctl_retro_scaling_caps_t     retroScalingCaps     = { 0 };
    ctl_retro_scaling_settings_t retroScalingSettings = { 0 };

    NULL_PTR_CHECK(argsRetroScalingSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScaling !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        retroScalingCaps.Size = sizeof(ctl_retro_scaling_caps_t);
        apiResult             = ControlApiGetSupportedRetroScalingCapability(hActDevices[adapterIndex], &retroScalingCaps);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiGetSupportedRetroScalingCapability Call Failed : 0x%X\n", apiResult);
            goto END;
        }
        DEBUG_LOG("ControlApiGetSupportedRetroScalingCapability Call Passed - Caps: 0x%X\n", retroScalingCaps.SupportedRetroScaling);

        if (FALSE == argsRetroScalingSettings->Get)
        {
            retroScalingSettings.Get              = argsRetroScalingSettings->Get;
            retroScalingSettings.RetroScalingType = argsRetroScalingSettings->RetroScalingType;
            retroScalingSettings.Enable           = argsRetroScalingSettings->Enable;
            retroScalingSettings.Size             = sizeof(ctl_retro_scaling_settings_t);

            apiResult = ControlApiGetSetRetroScaling(hActDevices[adapterIndex], &retroScalingSettings);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSetRetroScaling Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            DEBUG_LOG("ControlApiGetSetRetroScaling Passed Enable - 0x%x,  ScalingType:0x%x\n", retroScalingSettings.Enable, retroScalingSettings.RetroScalingType);
        }
        else
        {   
            retroScalingSettings.Get              = argsRetroScalingSettings->Get;
            retroScalingSettings.Enable           = argsRetroScalingSettings->Enable;
            retroScalingSettings.Size             = sizeof(ctl_retro_scaling_settings_t);

            apiResult = ControlApiGetSetRetroScaling(hActDevices[adapterIndex], &retroScalingSettings);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSupportedRetroScalingCapability Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            memcpy_s(argsRetroScalingSettings, argsRetroScalingSettings->Size, &retroScalingSettings, retroScalingSettings.Size);
            DEBUG_LOG("ControlApiGetSetRetroScaling Get Call Passed- 0x%x,  ScalingType:0x%x\n", retroScalingSettings.Enable, retroScalingSettings.RetroScalingType);
        }
    }

END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetSetEnduranceGaming(ctl_3d_feature_getset_t *argsGetSet3DFeature, ctl_endurance_gaming_t *argsEnduranceGaming, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult            = TRUE;
    bool                         displayAdapterStatus = TRUE;
    uint32_t                     adapterIndex         = 0;
    uint32_t                     adapterCount         = 0;
    uint32_t                     displayCount         = 0;
    uint32_t                     displayIndex         = 0;
    ctl_device_adapter_handle_t *hDevices             = nullptr;
    ctl_device_adapter_handle_t *hActDevices          = nullptr;
    ctl_display_output_handle_t *hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *hDisplayActive       = nullptr;
    ctl_3d_feature_getset_t      getSet3DFeature      = { 0 };

    NULL_PTR_CHECK(argsGetSet3DFeature);

    // Query Intel adapters list
    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        return apiResult;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetSetEnduranceGaming !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        getSet3DFeature.Size = sizeof(ctl_3d_feature_getset_t);

        if (FALSE == argsGetSet3DFeature->bSet)
        {
            getSet3DFeature.FeatureType     = CTL_3D_FEATURE_ENDURANCE_GAMING;
            getSet3DFeature.bSet            = argsGetSet3DFeature->bSet;
            getSet3DFeature.CustomValueSize = sizeof(ctl_endurance_gaming_t);
            getSet3DFeature.pCustomValue    = (ctl_endurance_gaming_t *)malloc(sizeof(ctl_endurance_gaming_t));
            getSet3DFeature.ValueType       = CTL_PROPERTY_VALUE_TYPE_CUSTOM;
            getSet3DFeature.Version         = 0;

            apiResult = ControlApiGetSet3DFeature(hActDevices[adapterIndex], &getSet3DFeature);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSet3DFeature Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            DEBUG_LOG("ControlApiGetSet3DFeature Passed Enable - 0x%x\n", getSet3DFeature.bSet);
            ctl_endurance_gaming_t *pGetEnduranceGaming = (ctl_endurance_gaming_t *)getSet3DFeature.pCustomValue;

            INFO_LOG(" EG Control = %d\n", pGetEnduranceGaming->EGControl);
            INFO_LOG(" EG mode = %d\n", pGetEnduranceGaming->EGMode);
        }
        else
        {
            ctl_endurance_gaming_t setEnduranceGaming;
            getSet3DFeature.FeatureType     = CTL_3D_FEATURE_ENDURANCE_GAMING;
            getSet3DFeature.bSet            = argsGetSet3DFeature->bSet;
            getSet3DFeature.CustomValueSize = sizeof(ctl_endurance_gaming_t);
            setEnduranceGaming.EGControl    = argsEnduranceGaming->EGControl;
            setEnduranceGaming.EGMode       = argsEnduranceGaming->EGMode;
            getSet3DFeature.pCustomValue    = &setEnduranceGaming;
            getSet3DFeature.ValueType       = CTL_PROPERTY_VALUE_TYPE_CUSTOM;
            getSet3DFeature.Version         = 0;

            INFO_LOG("EG Control %d \t EG mode %d", setEnduranceGaming.EGControl, setEnduranceGaming.EGMode);

            apiResult = ControlApiGetSet3DFeature(hActDevices[adapterIndex], &getSet3DFeature);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSet3DFeature for Endurance Gaming Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            DEBUG_LOG("ControlApiGetSet3DFeature for Endurance Gaming Call Passed\n");
        }
    }

END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetLace(ctl_lace_config_t *pGetLaceConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;
    ctl_lace_config_t            laceParams     = { 0 };

    NULL_PTR_CHECK(pGetLaceConfig);
    laceParams.Size = sizeof(ctl_lace_config_t);
    ctl_lace_lux_aggr_map_entry_t GetLuxVsArrgMap[51];
    laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable = GetLuxVsArrgMap;
    laceParams.OpTypeGet                                      = pGetLaceConfig->OpTypeGet;
    laceParams.Version                                        = 0;

    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetLace !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPIGetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                VERIFY_API_STATUS(ControlApiGetLaces(hDisplayActive[displayIndex], &laceParams));

                switch (laceParams.OpTypeGet)
                {
                case CTL_GET_OPERATION_FLAG_CURRENT:
                    INFO_LOG("Get Oepration: CTL_GET_OPERATION_FLAG_CURRENT \n");
                    if (laceParams.Trigger == 1)
                    {
                        INFO_LOG("Default OpMode: %d", laceParams.Trigger);
                        INFO_LOG("Default Number of entries: %d", laceParams.LaceConfig.AggrLevelMap.NumEntries);
                    }
                    else
                    {
                        INFO_LOG("Default OpMode: %d", laceParams.Trigger);
                    }
                    break;
                case CTL_GET_OPERATION_FLAG_DEFAULT:

                    INFO_LOG("Get Oepration: CTL_GET_OPERATION_FLAG_DEFAULT\n");
                    INFO_LOG("Default Number of entries: %d", laceParams.LaceConfig.AggrLevelMap.NumEntries);
                    if (laceParams.Trigger == 1)
                    {
                        INFO_LOG("Default OpMode: %d", laceParams.Trigger);
                    }
                    else
                    {
                        ERROR_LOG("Default OpMode is not Ambient Mode");
                        apiResult = FALSE;
                        goto END;
                    }
                    break;
                case CTL_GET_OPERATION_FLAG_CAPABILITY:

                    INFO_LOG("Get Oepration: CTL_GET_OPERATION_FLAG_CAPABILITY\n");
                    INFO_LOG("Max Number of entries supported: %d", laceParams.LaceConfig.AggrLevelMap.MaxNumEntries);
                    INFO_LOG("Supported TriggerType: %d", laceParams.Trigger);
                    break;
                default:
                    ERROR_LOG("Lace Get operation type not Supported \n");
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    return apiResult;
}

bool ControlAPIGetGamingFlipModes(ctl_3d_feature_getset_t *argsGetSet3DFeature, int setFlipMode, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult       = TRUE;
    uint32_t                     adapterIndex    = 0;
    uint32_t                     adapterCount    = 0;
    uint32_t                     displayCount    = 0;
    uint32_t                     displayIndex    = 0;
    ctl_device_adapter_handle_t *hDevices        = nullptr;
    ctl_device_adapter_handle_t *hActDevices     = nullptr;
    ctl_display_output_handle_t *hDisplayOutput  = nullptr;
    ctl_display_output_handle_t *hDisplayActive  = nullptr;
    ctl_3d_feature_getset_t      getSet3DFeature = { 0 };

    NULL_PTR_CHECK(argsGetSet3DFeature);

    // Query Intel adapters list
    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }
    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetGamingFlipModes !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        getSet3DFeature.Size = sizeof(ctl_3d_feature_getset_t);

        if (FALSE == argsGetSet3DFeature->bSet)
        {
            getSet3DFeature.FeatureType           = CTL_3D_FEATURE_GAMING_FLIP_MODES;
            getSet3DFeature.bSet                  = argsGetSet3DFeature->bSet;
            getSet3DFeature.CustomValueSize       = 0;
            getSet3DFeature.ApplicationName       = argsGetSet3DFeature->ApplicationName;
            getSet3DFeature.ApplicationNameLength = (int8_t)strlen(getSet3DFeature.ApplicationName);
            getSet3DFeature.ValueType             = CTL_PROPERTY_VALUE_TYPE_ENUM;
            getSet3DFeature.Version               = 0;

            apiResult = ControlApiGetSet3DFeature(hDevices[adapterIndex], &getSet3DFeature);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSet3DFeature Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            DEBUG_LOG("ControlApiGetSet3DFeature Passed Enable - 0x%x\n", getSet3DFeature.bSet);
            INFO_LOG("ctlGetSet3DFeature returned success(Get GamingFlipsCaps)\n");
        }
        else
        {
            getSet3DFeature.FeatureType               = CTL_3D_FEATURE_GAMING_FLIP_MODES;
            getSet3DFeature.bSet                      = argsGetSet3DFeature->bSet;
            getSet3DFeature.CustomValueSize           = 0;
            getSet3DFeature.ApplicationName           = argsGetSet3DFeature->ApplicationName;
            getSet3DFeature.ApplicationNameLength     = (int8_t)strlen(getSet3DFeature.ApplicationName);
            getSet3DFeature.ValueType                 = CTL_PROPERTY_VALUE_TYPE_ENUM;
            getSet3DFeature.Value.EnumType.EnableType = setFlipMode;
            getSet3DFeature.pCustomValue              = NULL;
            getSet3DFeature.Version                   = 0;

            INFO_LOG("Application Name %s", getSet3DFeature.ApplicationName);

            apiResult = ControlApiGetSet3DFeature(hDevices[adapterIndex], &getSet3DFeature);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetSet3DFeature Call Failed : 0x%x\n", apiResult);
                goto END;
            }
            DEBUG_LOG("ControlApiGetSet3DFeature Call Passed\n");
        }
    }
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetLace(ctl_lace_config_t *pSetLaceConfig, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;

    NULL_PTR_CHECK(pSetLaceConfig);
    ctl_lace_config_t laceParams = { 0 };
    laceParams.Size              = sizeof(ctl_lace_config_t);
    laceParams.Enabled           = TRUE;
    laceParams.OpTypeSet         = pSetLaceConfig->OpTypeSet;
    laceParams.Trigger           = pSetLaceConfig->Trigger;
    laceParams.Version           = 0;

    if (laceParams.OpTypeSet == CTL_SET_OPERATION_CUSTOM)
    {
        DEBUG_LOG("Set Operation: Custom");

        if (laceParams.Trigger == CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT)
        {
            //// Ambient Adaptive Mode
            // laceParams.LaceConfig = pSetLaceConfig->LaceConfig;
            laceParams.LaceConfig.AggrLevelMap.NumEntries = 6;
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable =
            (ctl_lace_lux_aggr_map_entry_t *)malloc(sizeof(ctl_lace_lux_aggr_map_entry_t) * laceParams.LaceConfig.AggrLevelMap.NumEntries);
            laceParams.Trigger                                           = CTL_LACE_TRIGGER_FLAG_AMBIENT_LIGHT;
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[0] = { 0, 0 };
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[1] = { 100, 10 };
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[2] = { 500, 30 };
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[3] = { 1000, 50 };
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[4] = { 5000, 70 };
            laceParams.LaceConfig.AggrLevelMap.pLuxToAggrMappingTable[5] = { 7000, 100 };
        }
        else
        {
            /// FixedAggressivenessLevelPercent
            laceParams.LaceConfig.FixedAggressivenessLevelPercent = pSetLaceConfig->LaceConfig.FixedAggressivenessLevelPercent;
        }
    }
    else if (laceParams.OpTypeSet == CTL_SET_OPERATION_RESTORE_DEFAULT)
    {
        DEBUG_LOG("Set Operation: Restore Default");
    }
    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
    NULL_PTR_CHECK(hDisplayActive);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
        goto END;
    }

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {

                apiResult = ControlApiSetLaces(hDisplayActive[displayIndex], &laceParams);

                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlAPI SetLace operation Failed\n");
                    goto END;
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    return apiResult;
}

bool ControlAPIGetOutputFormat(ctl_get_set_wire_format_config_t *pGetSetWireFormat, PANEL_INFO *pPanelInfo)
{
    bool                             apiResult                = TRUE;
    uint32_t                         adapterIndex             = 0;
    uint32_t                         adapterCount             = 0;
    uint32_t                         displayCount             = 0;
    uint32_t                         displayIndex             = 0;
    ctl_device_adapter_handle_t *    hDevices                 = nullptr;
    ctl_device_adapter_handle_t *    hActDevices              = nullptr;
    ctl_display_output_handle_t *    hDisplayOutput           = nullptr;
    ctl_display_output_handle_t *    hDisplayActive           = nullptr;
    ctl_lace_config_t                laceParams               = { 0 };
    ctl_get_set_wire_format_config_t CurrentWireFormatSetting = { 0 };
    ctl_get_set_wire_format_config_t NewWireFormatSetting     = { 0 };

    NULL_PTR_CHECK(pGetSetWireFormat);
    INFO_LOG("Control API EnumerateDisplayOutput Pass");
    CurrentWireFormatSetting.Size      = sizeof(ctl_get_set_wire_format_config_t);
    CurrentWireFormatSetting.Operation = CTL_WIRE_FORMAT_OPERATION_TYPE_GET;
    INFO_LOG("Current ColorModel %d", pPanelInfo->targetID);
    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
    NULL_PTR_CHECK(hDisplayActive);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    INFO_LOG("Control API EnumerateDevice Failed!!");
    INFO_LOG("Current ColorModel %d", pPanelInfo->targetID);
    if (FALSE == apiResult)
    {
        INFO_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
        goto END;
    }
    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                INFO_LOG("ctlGetSetWireFormat");
                DEBUG_LOG("Current TargetID %d", pPanelInfo->targetID);
                ControlAPIGetSetWireFormat(hDisplayActive[displayIndex], &CurrentWireFormatSetting);
                INFO_LOG("ctlGetSetWireFormat");
                DEBUG_LOG("Current TargetID %d", pPanelInfo->targetID);
                DEBUG_LOG("Current ColorDepth %d", CurrentWireFormatSetting.WireFormat.ColorDepth);
                DEBUG_LOG("Current Model %d", CurrentWireFormatSetting.WireFormat.ColorModel);

                for (uint32_t Index = 0; Index < CTL_MAX_WIREFORMAT_COLOR_MODELS_SUPPORTED; Index++)
                {
                    DEBUG_LOG("Supported ColorModel %d", CurrentWireFormatSetting.SupportedWireFormat[Index].ColorModel);
                    DEBUG_LOG("Supported ColorDepth %d", CurrentWireFormatSetting.SupportedWireFormat[Index].ColorDepth);
                }
                memcpy_s(pGetSetWireFormat, pGetSetWireFormat->Size, &CurrentWireFormatSetting, CurrentWireFormatSetting.Size);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    return apiResult;
}

bool ControlAPISetOutputFormat(ctl_get_set_wire_format_config_t *pGetSetWireFormat, PANEL_INFO *pPanelInfo)
{
    bool                             apiResult                = TRUE;
    uint32_t                         adapterIndex             = 0;
    uint32_t                         adapterCount             = 0;
    uint32_t                         displayCount             = 0;
    uint32_t                         displayIndex             = 0;
    ctl_device_adapter_handle_t *    hDevices                 = nullptr;
    ctl_device_adapter_handle_t *    hActDevices              = nullptr;
    ctl_display_output_handle_t *    hDisplayOutput           = nullptr;
    ctl_display_output_handle_t *    hDisplayActive           = nullptr;
    ctl_lace_config_t                laceParams               = { 0 };
    ctl_get_set_wire_format_config_t CurrentWireFormatSetting = { 0 };
    INFO_LOG("set");
    NULL_PTR_CHECK(pGetSetWireFormat);
    CurrentWireFormatSetting.Size                  = sizeof(ctl_get_set_wire_format_config_t);
    CurrentWireFormatSetting.Operation             = CTL_WIRE_FORMAT_OPERATION_TYPE_SET;
    CurrentWireFormatSetting.WireFormat.ColorModel = pGetSetWireFormat->WireFormat.ColorModel;
    CurrentWireFormatSetting.WireFormat.ColorDepth = pGetSetWireFormat->WireFormat.ColorDepth;
    DEBUG_LOG("Current ColorDepth %d", CurrentWireFormatSetting.WireFormat.ColorDepth);
    DEBUG_LOG("Current Model %d", CurrentWireFormatSetting.WireFormat.ColorModel);
    INFO_LOG("set");
    VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
    NULL_PTR_CHECK(hDisplayActive);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    INFO_LOG("Control API EnumerateDevice Failed!!");
    INFO_LOG("Current ColorModel %d", pPanelInfo->targetID);
    if (FALSE == apiResult)
    {
        INFO_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
        goto END;
    }
    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                INFO_LOG("ctlGetSetWireFormat");
                DEBUG_LOG("Current TargetID %d", pPanelInfo->targetID);
                ControlAPIGetSetWireFormat(hDisplayActive[displayIndex], &CurrentWireFormatSetting);
                INFO_LOG("ctlGetSetWireFormat");
                DEBUG_LOG("Current TargetID %d", pPanelInfo->targetID);
                DEBUG_LOG("Current ColorDepth %d", CurrentWireFormatSetting.WireFormat.ColorDepth);
                DEBUG_LOG("Current Model %d", CurrentWireFormatSetting.WireFormat.ColorModel);

                for (uint32_t Index = 0; Index < CTL_MAX_WIREFORMAT_COLOR_MODELS_SUPPORTED; Index++)
                {
                    DEBUG_LOG("Supported ColorModel %d", CurrentWireFormatSetting.SupportedWireFormat[Index].ColorModel);
                    DEBUG_LOG("Supported ColorDepth %d", CurrentWireFormatSetting.SupportedWireFormat[Index].ColorDepth);
                }
                memcpy_s(pGetSetWireFormat, pGetSetWireFormat->Size, &CurrentWireFormatSetting, CurrentWireFormatSetting.Size);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    return apiResult;
}

bool ControlAPIGetIntelArcSyncInfo(ctl_intel_arc_sync_monitor_params_t *argsMonitorParams, PANEL_INFO *pPanelInfo)
{
    bool                                apiResult      = TRUE;
    uint32_t                            adapterIndex   = 0;
    uint32_t                            adapterCount   = 0;
    uint32_t                            displayCount   = 0;
    uint32_t                            displayIndex   = 0;
    ctl_device_adapter_handle_t *       hDevices       = nullptr;
    ctl_device_adapter_handle_t *       hActDevices    = nullptr;
    ctl_display_output_handle_t *       hDisplayOutput = nullptr;
    ctl_display_output_handle_t *       hDisplayActive = nullptr;
    ctl_intel_arc_sync_monitor_params_t monitorParams  = { 0 };

    NULL_PTR_CHECK(argsMonitorParams);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetIntelArcSyncInfo !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlApiGetCurrentIntelArcSyncInfo Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlApiGetCurrentIntelArcSyncInfo: displayCount %d ", displayCount);

        if (NULL != hDisplayActive)
        {
            monitorParams.Size    = sizeof(ctl_intel_arc_sync_monitor_params_t);
            monitorParams.Version = 0;
            VERIFY_API_STATUS(ControlApiGetIntelArcSyncInfoForMonitor(*hDisplayActive, &monitorParams));
            DEBUG_LOG("ControlApiGetCurrentIntelArcSyncInfo Query Call Passed for targetID : %d\n", pPanelInfo->targetID);
            memcpy_s(argsMonitorParams, argsMonitorParams->Size, &monitorParams, monitorParams.Size);
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetIntelArcSyncProfile(ctl_intel_arc_sync_profile_params_t *argsProfileParams, PANEL_INFO *pPanelInfo)
{
    bool                                apiResult            = TRUE;
    uint32_t                            adapterIndex         = 0;
    uint32_t                            adapterCount         = 0;
    uint32_t                            displayCount         = 0;
    uint32_t                            displayIndex         = 0;
    ctl_device_adapter_handle_t *       hDevices             = nullptr;
    ctl_device_adapter_handle_t *       hActDevices          = nullptr;
    ctl_display_output_handle_t *       hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *       hDisplayActive       = nullptr;
    ctl_intel_arc_sync_profile_params_t arcSyncProfileParams = { 0 };

    NULL_PTR_CHECK(argsProfileParams);
    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPISetIntelArcSyncProfile !!!");
        goto END;
    }

    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPIApplyCustomIntelArcSyncProfile Call !!!");
            goto END;
        }
        DEBUG_LOG("ControlAPIApplyCustomIntelArcSyncProfile: Display_Count %d ", displayCount);

        if (NULL != hDisplayActive)
        {
            arcSyncProfileParams.Version             = 0;
            arcSyncProfileParams.Size                = sizeof(ctl_intel_arc_sync_profile_params_t);
            arcSyncProfileParams.IntelArcSyncProfile = argsProfileParams->IntelArcSyncProfile;
            if (argsProfileParams->IntelArcSyncProfile == CTL_INTEL_ARC_SYNC_PROFILE_CUSTOM)
            {
                arcSyncProfileParams.MaxFrameTimeDecreaseInUs = argsProfileParams->MaxFrameTimeDecreaseInUs;
                arcSyncProfileParams.MaxFrameTimeIncreaseInUs = argsProfileParams->MaxFrameTimeIncreaseInUs;
                arcSyncProfileParams.MinRefreshRateInHz       = argsProfileParams->MinRefreshRateInHz;
                arcSyncProfileParams.MaxRefreshRateInHz       = argsProfileParams->MaxRefreshRateInHz;
            }
            apiResult = ControlApiSetIntelArcSyncProfile(*hDisplayActive, &arcSyncProfileParams);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiSetIntelArcSyncProfile Call Failed for targetID %d: 0x%X\n", pPanelInfo->targetID, apiResult);
                goto END;
            }
            DEBUG_LOG("ControlAPISetIntelArcSyncProfile Success for targetID %d:", pPanelInfo->targetID);
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetCurrentArcSyncProfile(ctl_intel_arc_sync_profile_t *argsProfileParams, PANEL_INFO *pPanelInfo)
{
    bool                                apiResult            = TRUE;
    uint32_t                            adapterIndex         = 0;
    uint32_t                            adapterCount         = 0;
    uint32_t                            displayCount         = 0;
    uint32_t                            displayIndex         = 0;
    ctl_device_adapter_handle_t *       hDevices             = nullptr;
    ctl_device_adapter_handle_t *       hActDevices          = nullptr;
    ctl_display_output_handle_t *       hDisplayOutput       = nullptr;
    ctl_display_output_handle_t *       hDisplayActive       = nullptr;
    ctl_intel_arc_sync_profile_params_t arcSyncProfileParams = { 0 };

    NULL_PTR_CHECK(argsProfileParams);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetCurrentArcSyncProfile !!!");
        goto END;
    }
    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("ControlApiEnumerateDisplayOutputs Failed for Adapter - %d !!\n", adapterIndex);
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPIGetCurrentArcSyncProfile Call !!!");
            goto END;
        }
        DEBUG_LOG("GetCurrentArcSyncProfile: displayCount %d ", displayCount);
        if (NULL != hDisplayActive)
        {
            arcSyncProfileParams.Size = sizeof(ctl_intel_arc_sync_profile_params_t);
            apiResult                 = ControlApiGetIntelArcSyncProfile(*hDisplayActive, &arcSyncProfileParams);
            if (FALSE == apiResult)
            {
                ERROR_LOG("ControlApiGetIntelArcSyncProfile Call Failed for targetID %d : 0x%X\n", pPanelInfo->targetID, apiResult);
                goto END;
            }
            memcpy_s(argsProfileParams, sizeof(ctl_intel_arc_sync_profile_params_t), &arcSyncProfileParams, sizeof(ctl_intel_arc_sync_profile_params_t));
            DEBUG_LOG("ControlApiGetIntelArcSyncProfile Call Passed for targetID %d\n", pPanelInfo->targetID);
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPISetBrightnessSetting(ctl_set_brightness_t *argsSetBrightnessSettings, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult                 = TRUE;
    uint32_t                     adapterIndex              = 0;
    uint32_t                     adapterCount              = 0;
    uint32_t                     displayCount              = 0;
    uint32_t                     displayIndex              = 0;
    ctl_device_adapter_handle_t *hDevices                  = nullptr;
    ctl_device_adapter_handle_t *hActDevices               = nullptr;
    ctl_display_output_handle_t *hDisplayOutput            = nullptr;
    ctl_display_output_handle_t *hDisplayActive            = nullptr;
    ctl_set_brightness_t         SetBrightnessSettings     = { 0 };
    ctl_get_brightness_t         AppliedBrightnessSettings = { 0 };
    ctl_result_t                 Result                    = CTL_RESULT_SUCCESS;
    bool                         IsDisplayActive           = false;
    bool                         IsCompanionDisplay        = false;

    // display encoder properties
    ctl_adapter_display_encoder_properties_t displayEncoderArgs = { 0 };

    // display properties
    ctl_display_properties_t stdisplayproperties = {};
    stdisplayproperties.Size                     = sizeof(ctl_display_properties_t);

    NULL_PTR_CHECK(argsSetBrightnessSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    INFO_LOG("Api Result for Enumerate Devices:%d", apiResult);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScaling !!!");
        goto END;
    }

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {

        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {

                // check for companion display , SET/GET call should be called for only companion display.
                // Result = True;
                SetBrightnessSettings.Size                     = sizeof(ctl_set_brightness_t);
                SetBrightnessSettings.TargetBrightness         = argsSetBrightnessSettings->TargetBrightness;
                SetBrightnessSettings.SmoothTransitionTimeInMs = argsSetBrightnessSettings->SmoothTransitionTimeInMs;
                AppliedBrightnessSettings.Size                 = sizeof(ctl_get_brightness_t);

                apiResult = ControlApiSetBrightnessSettings(hDisplayActive[displayIndex], &SetBrightnessSettings);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlAPISetBrightnessSetting Call Failed for targetID %d: 0x%X\n", pPanelInfo->targetID, apiResult);
                    goto END;
                }
                DEBUG_LOG("ControlAPISetBrightnessSetting Success for targetID %d:", pPanelInfo->targetID);
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetBrightnessSetting(ctl_get_brightness_t *argsGetBrightnessSettings, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult             = TRUE;
    uint32_t                     adapterIndex          = 0;
    uint32_t                     adapterCount          = 0;
    uint32_t                     displayCount          = 0;
    uint32_t                     displayIndex          = 0;
    ctl_device_adapter_handle_t *hDevices              = nullptr;
    ctl_device_adapter_handle_t *hActDevices           = nullptr;
    ctl_display_output_handle_t *hDisplayOutput        = nullptr;
    ctl_display_output_handle_t *hDisplayActive        = nullptr;
    ctl_result_t                 Result                = CTL_RESULT_SUCCESS;
    ctl_get_brightness_t         GetBrightnessSettings = { 0 };
    GetBrightnessSettings.Size                         = argsGetBrightnessSettings->Size;

    INFO_LOG("Inside the Get_Brightness call");

    NULL_PTR_CHECK(argsGetBrightnessSettings);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    INFO_LOG("Api Result for Enumerate Devices:%d", apiResult);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!\n");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during ControlAPIGetScaling !!!");
        goto END;
    }

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {

        VERIFY_ONECORE_API_STATUS(!ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayActive);
        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayActive);
            continue;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during ControlAPISetLace Call !!!");
            goto END;
        }

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayActive[displayIndex])
            {
                apiResult = ControlApiGetBrightnessSettings(hDisplayActive[displayIndex], &GetBrightnessSettings);
                if (FALSE == apiResult)
                {
                    ERROR_LOG("ControlAPIGetBrightnessSetting Call Failed for targetID %d: 0x%X\n", pPanelInfo->targetID, apiResult);
                    goto END;
                }
                DEBUG_LOG("ControlAPIGetBrightnessSetting Success for targetID %d:", pPanelInfo->targetID);
                memcpy_s(argsGetBrightnessSettings, argsGetBrightnessSettings->Size, &GetBrightnessSettings, GetBrightnessSettings.Size);
                INFO_LOG("Current brightness = %d\n", GetBrightnessSettings.CurrentBrightness);
                INFO_LOG("Target brightness = %d\n", GetBrightnessSettings.TargetBrightness);
            }
        }
    }

END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIEDIDManagement(ctl_edid_management_args_t *argsEDIDManagement, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     adapterCount   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     displayIndex   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayTest   = nullptr;
    ctl_edid_management_args_t   EDIDmgmtargs   = { 0 };
    static uint8_t EdidOverrideBuf[] = { 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x10, 0xAC, 0x16, 0xF0, 0x4C, 0x4E, 0x37, 0x30, 0x17, 0x15, 0x01, 0x03, 0x80, 0x34,
                                         0x20, 0x78, 0xEA, 0x1E, 0xC5, 0xAE, 0x4F, 0x34, 0xB1, 0x26, 0x0E, 0x50, 0x54, 0xA5, 0x4B, 0x00, 0x81, 0x80, 0xA9, 0x40, 0xD1, 0x00,
                                         0x71, 0x4F, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x28, 0x3C, 0x80, 0xA0, 0x70, 0xB0, 0x23, 0x40, 0x30, 0x20, 0x36, 0x00,
                                         0x06, 0x44, 0x21, 0x00, 0x00, 0x1A, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x4A, 0x32, 0x35, 0x37, 0x4D, 0x31, 0x36, 0x31, 0x30, 0x37, 0x4E,
                                         0x4C, 0x0A, 0x00, 0x00, 0x00, 0xFC, 0x00, 0x49, 0x47, 0x43, 0x4C, 0x20, 0x44, 0x45, 0x4C, 0x55, 0x32, 0x34, 0x31, 0x30, 0x00, 0x00,
                                         0x00, 0xFD, 0x00, 0x38, 0x4C, 0x1E, 0x51, 0x11, 0x00, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x01, 0xEC, 0x02, 0x03, 0x29, 0xF1,
                                         0x50, 0x90, 0x05, 0x04, 0x03, 0x02, 0x07, 0x16, 0x01, 0x1F, 0x12, 0x13, 0x14, 0x20, 0x15, 0x11, 0x06, 0x23, 0x09, 0x07, 0x07, 0x67,
                                         0x03, 0x0C, 0x00, 0x10, 0x00, 0x38, 0x2D, 0x83, 0x01, 0x00, 0x00, 0xE3, 0x05, 0x03, 0x01, 0x02, 0x3A, 0x80, 0x18, 0x71, 0x38, 0x2D,
                                         0x40, 0x58, 0x2C, 0x45, 0x00, 0x06, 0x44, 0x21, 0x00, 0x00, 0x1E, 0x01, 0x1D, 0x80, 0x18, 0x71, 0x1C, 0x16, 0x20, 0x58, 0x2C, 0x25,
                                         0x00, 0x06, 0x44, 0x21, 0x00, 0x00, 0x9E, 0x01, 0x1D, 0x00, 0x72, 0x51, 0xD0, 0x1E, 0x20, 0x6E, 0x28, 0x55, 0x00, 0x06, 0x44, 0x21,
                                         0x00, 0x00, 0x1E, 0x8C, 0x0A, 0xD0, 0x8A, 0x20, 0xE0, 0x2D, 0x10, 0x10, 0x3E, 0x96, 0x00, 0x06, 0x44, 0x21, 0x00, 0x00, 0x18, 0x00,
                                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3E };
    uint32_t       EdidSize          = sizeof(EdidOverrideBuf);

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter in ControlAPIEDIDManagement() !!!");
        goto END;
    }

    DEBUG_LOG("Number of Adapters %d", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayOutput);
        hDisplayTest = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        NULL_PTR_CHECK(hDisplayTest);

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            FREE_MEMORY(hDisplayOutput);
            FREE_MEMORY(hDisplayTest);
            continue;
        }

        DEBUG_LOG("Enumerated Display Encoder Objects %d ", displayCount);

        apiResult = GetDisplayHandle(&displayCount, hDisplayOutput, hDisplayTest, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Display Handle !!!");
            goto END;
        }
        DEBUG_LOG("Display Handle Match With Target ID Count %d ", displayCount);

        for (displayIndex = 0; displayIndex < displayCount; displayIndex++)
        {
            if (NULL != hDisplayTest[displayIndex])
            {
                switch (argsEDIDManagement->OpType)
                {
                case CTL_EDID_MANAGEMENT_OPTYPE_READ_EDID:
                    DEBUG_LOG("ControlAPIEDIDManagement: Read Edid");
                    EDIDmgmtargs.Size     = sizeof(ctl_edid_management_args_t);
                    EDIDmgmtargs.Version  = 0; // Dummy value
                    EDIDmgmtargs.OpType   = argsEDIDManagement->OpType;
                    EDIDmgmtargs.EdidType = argsEDIDManagement->EdidType;
                    EDIDmgmtargs.EdidSize = argsEDIDManagement->EdidSize;

                    apiResult = ControlAPIEDIDManagementEx(hDisplayTest[displayIndex], &EDIDmgmtargs);
                    DEBUG_LOG("EDID management CAPI called for optype %d and outflag %d", argsEDIDManagement->OpType, argsEDIDManagement->OutFlags);
                    break;

                case CTL_EDID_MANAGEMENT_OPTYPE_LOCK_EDID:
                    DEBUG_LOG("ControlAPIEDIDManagement: Lock Edid");
                    EDIDmgmtargs.Size     = sizeof(ctl_edid_management_args_t);
                    EDIDmgmtargs.Version  = 0; // Dummy value
                    EDIDmgmtargs.OpType   = argsEDIDManagement->OpType;
                    EDIDmgmtargs.EdidType = argsEDIDManagement->EdidType;
                    EDIDmgmtargs.EdidSize = argsEDIDManagement->EdidSize;
                    EDIDmgmtargs.pEdidBuf = argsEDIDManagement->pEdidBuf;

                    // Lock can be called with monitor EDID or override / supplied edid. For supplied edid type , pEdidBuf and pEdidSize has to be updated in DLL
                    // This will be similar to Override OPTYPE

                    if (argsEDIDManagement->EdidType == CTL_EDID_TYPE_OVERRIDE)
                    {
                        EDIDmgmtargs.EdidSize = EdidSize;
                        EDIDmgmtargs.pEdidBuf = EdidOverrideBuf;
                    }

                    apiResult = ControlAPIEDIDManagementEx(hDisplayTest[displayIndex], &EDIDmgmtargs);
                    DEBUG_LOG("EDID management CAPI called for optype %d and outflag %d", argsEDIDManagement->OpType, argsEDIDManagement->OutFlags);
                    break;

                case CTL_EDID_MANAGEMENT_OPTYPE_UNLOCK_EDID:
                    DEBUG_LOG("ControlAPIEDIDManagement: Unlock Edid");
                    EDIDmgmtargs.Size     = sizeof(ctl_edid_management_args_t);
                    EDIDmgmtargs.Version  = 0; // Dummy value
                    EDIDmgmtargs.OpType   = argsEDIDManagement->OpType;
                    EDIDmgmtargs.EdidType = argsEDIDManagement->EdidType;
                    EDIDmgmtargs.EdidSize = argsEDIDManagement->EdidSize;
                    EDIDmgmtargs.pEdidBuf = argsEDIDManagement->pEdidBuf;

                    apiResult = ControlAPIEDIDManagementEx(hDisplayTest[displayIndex], &EDIDmgmtargs);
                    DEBUG_LOG("EDID management CAPI called for optype %d and outflag %d", argsEDIDManagement->OpType, argsEDIDManagement->OutFlags);
                    break;
                case CTL_EDID_MANAGEMENT_OPTYPE_OVERRIDE_EDID:
                    DEBUG_LOG("ControlAPIEDIDManagement: Override Edid");
                    EDIDmgmtargs.Size     = sizeof(ctl_edid_management_args_t);
                    EDIDmgmtargs.Version  = 0; // Dummy value
                    EDIDmgmtargs.OpType   = argsEDIDManagement->OpType;
                    EDIDmgmtargs.EdidType = argsEDIDManagement->EdidType;
                    EDIDmgmtargs.EdidSize = EdidSize;
                    EDIDmgmtargs.pEdidBuf = EdidOverrideBuf;

                    apiResult = ControlAPIEDIDManagementEx(hDisplayTest[displayIndex], &EDIDmgmtargs);
                    DEBUG_LOG("EDID management CAPI called for optype %d and outflag %d", argsEDIDManagement->OpType, argsEDIDManagement->OutFlags);
                    break;
                case CTL_EDID_MANAGEMENT_OPTYPE_UNDO_OVERRIDE_EDID:
                    DEBUG_LOG("ControlAPIEDIDManagement: Remove Edid");
                    EDIDmgmtargs.Size     = sizeof(ctl_edid_management_args_t);
                    EDIDmgmtargs.Version  = 0; // Dummy value
                    EDIDmgmtargs.OpType   = argsEDIDManagement->OpType;
                    EDIDmgmtargs.EdidType = argsEDIDManagement->EdidType;
                    EDIDmgmtargs.EdidSize = argsEDIDManagement->EdidSize;
                    EDIDmgmtargs.pEdidBuf = argsEDIDManagement->pEdidBuf;

                    apiResult = ControlAPIEDIDManagementEx(hDisplayTest[displayIndex], &EDIDmgmtargs);
                    DEBUG_LOG("EDID management CAPI called for optype %d and outflag %d", argsEDIDManagement->OpType, argsEDIDManagement->OutFlags);
                    break;
                default:
                    DEBUG_LOG("EDID management CAPI called for unknown optype %d", argsEDIDManagement->OpType);
                }
            }
        }
    }
END:
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayTest);
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool InitGenlockArgs(ctl_device_adapter_handle_t *hDevices, uint32_t AdapterCount, ctl_genlock_args_t *argsGenlock, ctl_genlock_args_t *pGenlockArgs)
{

    bool                         apiResult             = TRUE;
    ctl_device_adapter_handle_t  hFailureDeviceAdapter = nullptr;
    ctl_display_output_handle_t *hDisplayOutput        = nullptr;
    ctl_display_output_handle_t *hActiveDisplayOutputs = nullptr;
    uint32_t                     DisplayCount          = 0;
    uint8_t                      ActiveDisplayCount    = 0;
    uint8_t                      MaxNumDisplayOutputs  = 0;
    bool                         IsDisplayActive       = false;
    bool                         IsDisplayAttached     = false;
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex]                                    = { 0 };
        pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays = 0;
        pGenlockArgs[AdapterIndex].Operation                          = CTL_GENLOCK_OPERATION_VALIDATE;
    }
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        ActiveDisplayCount                                            = 0;
        MaxNumDisplayOutputs                                          = pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays;
        pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays = 0;

        // Enumerate all the possible target displays for the adapters
        // First step is to get the count
        DisplayCount = 0;
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hDevices[AdapterIndex], &DisplayCount, hDisplayOutput));

        if (DisplayCount <= 0)
        {
            DEBUG_LOG("Invalid Display Count. Skipping display enumeration for adapter: %d\n", AdapterIndex);
            continue;
        }

        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * DisplayCount);
        NULL_PTR_CHECK(hDisplayOutput);

        hActiveDisplayOutputs = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * MaxNumDisplayOutputs);
        NULL_PTR_CHECK(hActiveDisplayOutputs);
        memset(hActiveDisplayOutputs, 0, sizeof(ctl_display_output_handle_t) * MaxNumDisplayOutputs);

        apiResult = ControlApiEnumerateDisplayOutputs(hDevices[AdapterIndex], &DisplayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDevice Failed!!");
            goto Exit;
        }

        for (uint8_t DisplayIndex = 0; DisplayIndex < DisplayCount; DisplayIndex++)
        {
            ctl_display_properties_t stDisplayProperties = {};
            stDisplayProperties.Size                     = sizeof(ctl_display_properties_t);

            if (NULL == hDisplayOutput[DisplayIndex])
            {
                ERROR_LOG("hDisplayOutput[%d] is NULL.\n", DisplayIndex);
                apiResult = FALSE;
                goto Exit;
            }

            apiResult = ControlApiGetDisplayProperties(hDisplayOutput[DisplayIndex], &stDisplayProperties);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API get display properties Failed!!");
                goto Exit;
            }

            ctl_adapter_display_encoder_properties_t stDisplayEncoderProperties = {};
            stDisplayEncoderProperties.Size                                     = sizeof(ctl_adapter_display_encoder_properties_t);

            apiResult = ControlApiGetDisplayEncoderProperties(hDisplayOutput[DisplayIndex], &stDisplayEncoderProperties);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API get display encoder properties Failed!!");
                goto Exit;
            }

            IsDisplayActive   = stDisplayProperties.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ACTIVE;
            IsDisplayAttached = stDisplayProperties.DisplayConfigFlags & CTL_DISPLAY_CONFIG_FLAG_DISPLAY_ATTACHED;

            // Filter active display outputs
            if (IsDisplayActive && IsDisplayAttached)
            {
                hActiveDisplayOutputs[ActiveDisplayCount++] = hDisplayOutput[DisplayIndex];
            }
        }

        if (0 == ActiveDisplayCount)
        {
            DEBUG_LOG("There are no active displays for the selected port. ActiveDisplayCount is %d.\n", ActiveDisplayCount);
            apiResult = false;
            goto Exit;
        }

        pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays     = ActiveDisplayCount;
        pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem = argsGenlock->GenlockTopology.IsPrimaryGenlockSystem;

        // Allocate dynamic memories
        pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo =
        (ctl_genlock_display_info_t *)malloc(sizeof(ctl_genlock_display_info_t) * pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays);
        NULL_PTR_CHECK(pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo);
        memset(pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo, 0,
               sizeof(ctl_genlock_display_info_t) * pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays);

        pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList =
        (ctl_genlock_target_mode_list_t *)malloc(sizeof(ctl_genlock_target_mode_list_t) * pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays);
        NULL_PTR_CHECK(pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList);
        memset(pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList, 0,
               sizeof(ctl_genlock_target_mode_list_t) * pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays);

        for (uint8_t DisplayIndex = 0; DisplayIndex < ActiveDisplayCount; DisplayIndex++)
        {
            pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo[DisplayIndex].hDisplayOutput = hActiveDisplayOutputs[DisplayIndex];
            pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[DisplayIndex].hDisplayOutput    = hActiveDisplayOutputs[DisplayIndex];
        }
        // Free dynamically allocated memories
        FREE_MEMORY(hActiveDisplayOutputs);
        FREE_MEMORY(hDisplayOutput);
    }
Exit:
    // Free dynamically allocated memories
    FREE_MEMORY(hActiveDisplayOutputs);
    FREE_MEMORY(hDisplayOutput);
    return apiResult;
}

bool TestGenlockGetTimingDetails(ctl_device_adapter_handle_t *hDevices, ctl_genlock_args_t *pGenlockArgs, uint32_t AdapterCount)
{
    bool                            apiResult = TRUE;
    ctl_genlock_target_mode_list_t *pGenlockModeList;
    ctl_device_adapter_handle_t     hFailureDeviceAdapter = nullptr;

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_GET_TIMING_DETAILS;
        for (uint8_t ModeListIndex = 0; ModeListIndex < pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays; ModeListIndex++)
        {
            pGenlockModeList           = &pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[ModeListIndex];
            pGenlockModeList->NumModes = 0;
        }
    }

    // Get number of target modes
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        for (uint8_t ModeListIndex = 0; ModeListIndex < pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays; ModeListIndex++)
        {
            pGenlockModeList = &pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[ModeListIndex];
            if (NULL == pGenlockModeList->pTargetModes)
            {
                pGenlockModeList->pTargetModes = (ctl_display_timing_t *)malloc(pGenlockModeList->NumModes * sizeof(ctl_display_timing_t));
                NULL_PTR_CHECK(pGenlockModeList->pTargetModes);
            }
        }
    }

    // Get mode timings details
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }

    // @TODO: Remove below statement later. Keeping these log messages until ControlAPIGetAllDisplayTimingsGenlock() is stabilized.
    // Print mode timings details for all displays across adapters
    ctl_display_timing_t *pTargetModes = NULL;
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        for (uint8_t genlock_display = 0; genlock_display < pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays; genlock_display++)
        {
            INFO_LOG("=============================Genlock display #%d=============================", genlock_display);
            pGenlockModeList = &pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[genlock_display];
            if (NULL == pGenlockModeList->pTargetModes)
            {
                ERROR_LOG("pGenlockModeList->pTargetModes is null");
                continue;
            }

            INFO_LOG("GENLOCK MODELIST for display %p with total number of modes: %u", pGenlockModeList->hDisplayOutput, pGenlockModeList->NumModes);
            INFO_LOG("%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s%-25s", "Mode", "HActive", "VActive", "Pixelclock", "HTotal", "VTotal", "HBlank", "VBlank",
                     "HSync", "Vsync", "RefreshRate", "SignalStandard", "VicId");

            for (uint32_t num_modes = 0; num_modes < pGenlockModeList->NumModes; num_modes++)
            {
                pTargetModes = &pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[genlock_display].pTargetModes[num_modes];
                INFO_LOG("%-25lu%-25lu%-25lu%-25llu%-25lu%-25lu%-25lu%-25lu%-25lu%-25lu%-25f%-25lu%-25u", num_modes, pTargetModes->HActive, pTargetModes->VActive,
                         pTargetModes->PixelClock, pTargetModes->HTotal, pTargetModes->VTotal, pTargetModes->HBlank, pTargetModes->VBlank, pTargetModes->HSync, pTargetModes->VSync,
                         pTargetModes->RefreshRate, pTargetModes->SignalStandard, pTargetModes->VicId);
            }
        }
    }

Exit:
    return apiResult;
}

bool FindBestCommonTiming(ctl_genlock_args_t *pGenlockArgs, uint32_t AdapterCount)
{
    bool                            apiResult             = TRUE;
    ctl_genlock_target_mode_list_t *pGenlockModeListFixed = nullptr;
    ctl_genlock_target_mode_list_t *pGenlockModeList      = nullptr;
    ctl_display_timing_t *          pTargetModes          = nullptr;
    ctl_display_timing_t *          pPreferredTargetMode  = nullptr;
    uint8_t                         ModeIndex             = 0;

    // Find the best mode timing in the first display
    pGenlockModeListFixed = &pGenlockArgs[0].GenlockTopology.pGenlockModeList[0];
    for (ModeIndex = 0; ModeIndex < pGenlockModeListFixed->NumModes; ModeIndex++)
    {
        pTargetModes = &pGenlockModeListFixed->pTargetModes[ModeIndex];
        if ((NULL == pPreferredTargetMode) || ((pTargetModes->HActive >= pPreferredTargetMode->HActive) && (pTargetModes->VActive >= pPreferredTargetMode->VActive) &&
                                               (pTargetModes->RefreshRate > pPreferredTargetMode->RefreshRate)))
        {
            pPreferredTargetMode = pTargetModes;
        }
    }

    if (NULL == pPreferredTargetMode)
    {
        apiResult = FALSE;
        goto Exit;
    }
    pGenlockArgs[0].GenlockTopology.CommonTargetMode = *pPreferredTargetMode;

    // Check if the preferred mode timing is common in the first adapter
    for (uint8_t DisplayIndex = 1; DisplayIndex < pGenlockArgs[0].GenlockTopology.NumGenlockDisplays; DisplayIndex++)
    {
        pGenlockModeList = &pGenlockArgs[0].GenlockTopology.pGenlockModeList[DisplayIndex];
        for (ModeIndex = 0; ModeIndex < pGenlockModeList->NumModes; ModeIndex++)
        {
            pTargetModes = &pGenlockModeListFixed->pTargetModes[ModeIndex];
            if ((pPreferredTargetMode->PixelClock == pTargetModes->PixelClock) && (pPreferredTargetMode->HActive == pTargetModes->HActive) &&
                (pPreferredTargetMode->HTotal == pTargetModes->HTotal) && (pPreferredTargetMode->VActive == pTargetModes->VActive) &&
                (pPreferredTargetMode->VTotal == pTargetModes->VTotal) && (pPreferredTargetMode->RefreshRate == pTargetModes->RefreshRate))
            {
                break;
            }
        }
        if (ModeIndex == pGenlockModeList->NumModes)
        {
            pPreferredTargetMode = NULL;
            apiResult            = FALSE;
            goto Exit;
        }
    }

    // Check if the preferred mode of the 1st adapter is common among displays on all other adapters
    for (uint32_t AdapterIndex = 1; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        for (uint8_t DisplayIndex = 0; DisplayIndex < pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays; DisplayIndex++)
        {
            pGenlockModeList = &pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockModeList[DisplayIndex];
            for (ModeIndex = 0; ModeIndex < pGenlockModeList->NumModes; ModeIndex++)
            {
                pTargetModes = &pGenlockModeListFixed->pTargetModes[ModeIndex];
                if ((pPreferredTargetMode->PixelClock == pTargetModes->PixelClock) && (pPreferredTargetMode->HActive == pTargetModes->HActive) &&
                    (pPreferredTargetMode->HTotal == pTargetModes->HTotal) && (pPreferredTargetMode->VActive == pTargetModes->VActive) &&
                    (pPreferredTargetMode->VTotal == pTargetModes->VTotal) && (pPreferredTargetMode->RefreshRate == pTargetModes->RefreshRate))
                {
                    break;
                }
            }
            if (ModeIndex == pGenlockModeList->NumModes)
            {
                pPreferredTargetMode = NULL;
                apiResult            = FALSE;
                goto Exit;
            }
        }

        if (NULL == pPreferredTargetMode)
        {
            apiResult = FALSE;
            goto Exit;
        }
        else
        {
            pGenlockArgs[AdapterIndex].GenlockTopology.CommonTargetMode = *pPreferredTargetMode;
        }
    }

Exit:
    return apiResult;
}
bool TestGenlockValidate(ctl_device_adapter_handle_t *hDevices, ctl_genlock_args_t *pGenlockArgs, ctl_genlock_args_t *argsGenlock, uint32_t AdapterCount)
{
    bool                        apiResult             = TRUE;
    ctl_device_adapter_handle_t hFailureDeviceAdapter = nullptr;

    apiResult = TestGenlockGetTimingDetails(hDevices, pGenlockArgs, AdapterCount);
    if (FALSE == apiResult)
    {
        ERROR_LOG("TestGenlockGetTimingDetails Failed!!");
        goto Exit;
    }
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_VALIDATE;
        if (true == pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem)
        {
            pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo[0].IsPrimary = true;
        }
    }
    apiResult = FindBestCommonTiming(pGenlockArgs, AdapterCount);
    if (FALSE == apiResult)
    {
        ERROR_LOG("FindBestCommonTiming Failed!!");
        goto Exit;
    }
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        argsGenlock->IsGenlockPossible = pGenlockArgs[AdapterIndex].IsGenlockPossible;
    }
Exit:
    return apiResult;
}

bool TestGenlockGetTopology(ctl_device_adapter_handle_t *hDevices, ctl_genlock_args_t *pGenlockArgs, ctl_genlock_args_t *argsGenlock, uint32_t AdapterCount)
{
    bool                        apiResult             = TRUE;
    ctl_device_adapter_handle_t hFailureDeviceAdapter = nullptr;

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_GET_TOPOLOGY;
    }
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        argsGenlock->IsGenlockEnabled  = pGenlockArgs[AdapterIndex].IsGenlockEnabled;
        argsGenlock->IsGenlockPossible = pGenlockArgs[AdapterIndex].IsGenlockPossible;

        if (true == pGenlockArgs[AdapterIndex].IsGenlockEnabled)
        {
            argsGenlock->GenlockTopology.IsPrimaryGenlockSystem = pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem;
            argsGenlock->GenlockTopology.NumGenlockDisplays     = pGenlockArgs[AdapterIndex].GenlockTopology.NumGenlockDisplays;
        }
    }

Exit:
    return apiResult;
}
bool TestGenlockDisable(ctl_device_adapter_handle_t *hDevices, ctl_genlock_args_t *pGenlockArgs, ctl_genlock_args_t *argsGenlock, uint32_t AdapterCount)
{
    bool                        apiResult             = TRUE;
    ctl_device_adapter_handle_t hFailureDeviceAdapter = NULL;

    apiResult = TestGenlockValidate(hDevices, pGenlockArgs, argsGenlock, AdapterCount);
    if (FALSE == apiResult)
    {
        ERROR_LOG("TestGenlockValidate Failed!!");
        goto Exit;
    }

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_DISABLE;
        if (true == pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem)
        {
            pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo[0].IsPrimary = true;
        }
    }

    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_GET_TOPOLOGY;
    }
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }
    apiResult = TestGenlockGetTopology(hDevices, pGenlockArgs, argsGenlock, AdapterCount);

Exit:
    return apiResult;
}

bool TestGenlockEnable(ctl_device_adapter_handle_t *hDevices, ctl_genlock_args_t *pGenlockArgs, ctl_genlock_args_t *argsGenlock, uint32_t AdapterCount)
{
    bool                        apiResult             = TRUE;
    ctl_device_adapter_handle_t hFailureDeviceAdapter = NULL;

    apiResult = TestGenlockValidate(hDevices, pGenlockArgs, argsGenlock, AdapterCount);
    if (FALSE == apiResult)
    {
        ERROR_LOG("TestGenlockValidate Failed!!");
        goto Exit;
    }

    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_ENABLE;
        if (true == pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem)
        {
            pGenlockArgs[AdapterIndex].GenlockTopology.pGenlockDisplayInfo[0].IsPrimary = true;
        }
    }

    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }
    for (uint32_t AdapterIndex = 0; AdapterIndex < AdapterCount; AdapterIndex++)
    {
        pGenlockArgs[AdapterIndex].Operation = CTL_GENLOCK_OPERATION_GET_TOPOLOGY;
    }
    apiResult = ControlAPIGetSetDisplayGenlockEx(hDevices, pGenlockArgs, AdapterCount, &hFailureDeviceAdapter);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API Get Set DisplayGenlock Failed!!");
        goto Exit;
    }
    apiResult = TestGenlockGetTopology(hDevices, pGenlockArgs, argsGenlock, AdapterCount);

Exit:
    return apiResult;
}

bool ControlAPIGetSetDisplayGenlock(ctl_genlock_args_t *argsGenlock, PANEL_INFO *pPanelInfo)
{
    bool apiResult = TRUE;

    uint32_t adapterIndex          = 0;
    uint32_t adapterCount          = 0;
    uint32_t displayCount          = 0;
    uint32_t displayIndex          = 0;
    uint8_t  SecondaryAdapterCount = 0;

    ctl_device_adapter_handle_t *hDevices           = nullptr;
    ctl_device_adapter_handle_t *hActDevices        = nullptr;
    ctl_device_adapter_handle_t  hPrimaryAdapter    = nullptr;
    ctl_device_adapter_handle_t *hSecondaryAdapters = nullptr;

    ctl_genlock_args_t *pGenlockArgs = nullptr;

    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    apiResult   = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);

    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        FREE_MEMORY(hDevices);
        return FALSE;
    }
    if (FALSE == GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID))
    {
        ERROR_LOG("Failed to get Active Adapter in ControlAPIGetSetDisplayGenlock() !!!");
        goto END;
    }

    pGenlockArgs = (ctl_genlock_args_t *)malloc(sizeof(ctl_genlock_args_t) * adapterCount);
    NULL_PTR_CHECK(pGenlockArgs)

    switch (argsGenlock->Operation)
    {
    case CTL_GENLOCK_OPERATION_VALIDATE:
        apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
        apiResult = TestGenlockValidate(hActDevices, pGenlockArgs, argsGenlock, adapterCount);
        break;
    case CTL_GENLOCK_OPERATION_ENABLE:
        // The primary adapter must be enabled first before other secondary adapters are enabled
        if (true == argsGenlock->GenlockTopology.IsPrimaryGenlockSystem)
        {
            // Enable primary target on the primary adapter#0
            apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);

            // Select pipe#0 as primary pipe
            pGenlockArgs[0].GenlockTopology.pGenlockDisplayInfo[0].IsPrimary = true;

            apiResult = TestGenlockEnable(hActDevices, pGenlockArgs, argsGenlock, adapterCount);

            if (adapterCount >= 2)
            {
                // Other adapters are secondary systems for Genlock
                pGenlockArgs[0].GenlockTopology.pGenlockDisplayInfo[0].IsPrimary = false;
                argsGenlock->GenlockTopology.IsPrimaryGenlockSystem              = false;

                apiResult = InitGenlockArgs(&hActDevices[1], adapterCount - 1, argsGenlock, pGenlockArgs);
                apiResult = TestGenlockEnable(&hActDevices[1], pGenlockArgs, argsGenlock, adapterCount - 1);
            }
        }
        else
        {
            apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
            apiResult = TestGenlockEnable(hActDevices, pGenlockArgs, argsGenlock, adapterCount);
        }
        break;
    case CTL_GENLOCK_OPERATION_DISABLE:
        // The primary adapter must be disabled last after secondary adapters are disabled
        if (true == argsGenlock->GenlockTopology.IsPrimaryGenlockSystem)
        {
            if (adapterCount >= 2)
            {
                // Secondary adapters should be disabled first
                // Get topology to check which adapter is a primary
                apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
                apiResult = TestGenlockGetTopology(hActDevices, pGenlockArgs, argsGenlock, adapterCount);

                hSecondaryAdapters    = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount - 1);
                SecondaryAdapterCount = 0;

                for (uint32_t AdapterIndex = 0; AdapterIndex < adapterCount; AdapterIndex++)
                {
                    if (true == pGenlockArgs[AdapterIndex].GenlockTopology.IsPrimaryGenlockSystem)
                    {
                        hPrimaryAdapter = hDevices[AdapterIndex];
                    }
                    else if (true == pGenlockArgs[AdapterIndex].IsGenlockEnabled)
                    {
                        hSecondaryAdapters[SecondaryAdapterCount++] = hDevices[AdapterIndex];
                    }
                }

                argsGenlock->GenlockTopology.IsPrimaryGenlockSystem = false;
                // Disable secondary adapters
                if (0 != SecondaryAdapterCount)
                {
                    apiResult = InitGenlockArgs(hSecondaryAdapters, SecondaryAdapterCount, argsGenlock, pGenlockArgs);
                    apiResult = TestGenlockDisable(hSecondaryAdapters, pGenlockArgs, argsGenlock, SecondaryAdapterCount);
                }
                FREE_MEMORY(hSecondaryAdapters);
                argsGenlock->GenlockTopology.IsPrimaryGenlockSystem = true;
            }
            else
            {
                hPrimaryAdapter = hActDevices[0];
            }

            // Disable primary adapter
            apiResult = InitGenlockArgs(&hPrimaryAdapter, 1, argsGenlock, pGenlockArgs);
            apiResult = TestGenlockDisable(&hPrimaryAdapter, pGenlockArgs, argsGenlock, 1);
        }
        else
        {
            apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
            apiResult = TestGenlockDisable(hActDevices, pGenlockArgs, argsGenlock, adapterCount);
        }
        break;
    case CTL_GENLOCK_OPERATION_GET_TOPOLOGY:
        apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
        apiResult = TestGenlockGetTopology(hActDevices, pGenlockArgs, argsGenlock, adapterCount);
        break;
    default:
        DEBUG_LOG("GetSetDisplayGenlock CAPI called for unknown optype %d", argsGenlock->Operation);
    }
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    return apiResult;
}

bool ControlAPIGetAllDisplayTimingsGenlock(ctl_genlock_args_t *argsGenlock, GFX_ADAPTER_INFO gfxAdapterInfo)
{
    bool                         apiResult    = TRUE;
    uint32_t                     adapterCount = 0;
    ctl_device_adapter_handle_t *hDevices     = nullptr;
    ctl_device_adapter_handle_t *hActDevices  = nullptr;

    ctl_genlock_args_t *pGenlockArgs = nullptr;

    if (CTL_GENLOCK_OPERATION_GET_TIMING_DETAILS != argsGenlock->Operation)
    {
        ERROR_LOG("Unsupported operation %d for ControlAPIGetAllDisplayTimingsGenlock()", argsGenlock->Operation);
        apiResult = FALSE;
        goto END;
    }

    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    INFO_LOG("Identified adapters count = %d", adapterCount);

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    if (NULL == hDevices)
    {
        ERROR_LOG("Failed to allocate memory for hDevices");
        goto END;
    }
    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed with error code - %d", apiResult);
        goto END;
    }

    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    if (NULL == hActDevices)
    {
        ERROR_LOG("Failed to allocate memory for hActDevices");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, gfxAdapterInfo.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter in ControlAPIGetSetDisplayGenlock() !!!");
        goto END;
    }

    pGenlockArgs = (ctl_genlock_args_t *)malloc(sizeof(ctl_genlock_args_t) * adapterCount);
    if (NULL == pGenlockArgs)
    {
        ERROR_LOG("Failed to allocate memory for pGenlockArgs");
        goto END;
    }

    apiResult = InitGenlockArgs(hActDevices, adapterCount, argsGenlock, pGenlockArgs);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to initialize Genlock args ControlAPIGetSetDisplayGenlock() !!!");
        goto END;
    }

    apiResult = TestGenlockGetTimingDetails(hDevices, pGenlockArgs, adapterCount);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get timing details in ControlAPIGetSetDisplayGenlock() !!!");
        goto END;
    }

    // Copy required data from escape
    INFO_LOG("START: Copying Timings data from genlock args to input pointer!!");
    argsGenlock->GenlockTopology.NumGenlockDisplays = pGenlockArgs->GenlockTopology.NumGenlockDisplays;

    memcpy(&argsGenlock->GenlockTopology.pGenlockDisplayInfo, &pGenlockArgs->GenlockTopology.pGenlockDisplayInfo, sizeof(pGenlockArgs->GenlockTopology.pGenlockDisplayInfo));
    memcpy(&argsGenlock->GenlockTopology.pGenlockModeList, &pGenlockArgs->GenlockTopology.pGenlockModeList, sizeof(pGenlockArgs->GenlockTopology.pGenlockModeList));
    INFO_LOG("END:   Copying Timings data from genlock args to input pointer!!");

END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(pGenlockArgs);
    return apiResult;
}

bool GetTargetDisplayHandle(ctl_display_output_handle_t *htargetDisplay, PANEL_INFO *pPanelInfo)
{
    bool                         apiResult      = TRUE;
    uint32_t                     displayIndex   = 0;
    uint32_t                     adapterIndex   = 0;
    uint32_t                     displayCount   = 0;
    uint32_t                     adapterCount   = 0;
    ctl_device_adapter_handle_t *hDevices       = nullptr;
    ctl_device_adapter_handle_t *hActDevices    = nullptr;
    ctl_display_output_handle_t *hDisplayOutput = nullptr;
    ctl_display_output_handle_t *hDisplayActive = nullptr;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));
    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    if (NULL == hActDevices)
    {
        ERROR_LOG("Failed to allocate memory for hActDevices");
        goto END;
    }

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    apiResult = GetActiveAdapter(&adapterCount, hDevices, hActDevices, pPanelInfo->gfxAdapter.deviceID);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Failed to get Active Adapter during GetTargetDisplayHandle()!!!");
        goto END;
    }

    INFO_LOG("GetTargetDisplayHandle() adapterCount %d ", adapterCount);

    for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
    {
        // Enumerate all the possible target display's for the adapters
        displayCount = 0;
        VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));
        hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        if (NULL == hDisplayOutput)
        {
            ERROR_LOG("Failed to allocate memory for hDisplayOutput");
            continue;
        }

        hDisplayActive = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
        if (NULL == hDisplayActive)
        {
            ERROR_LOG("Failed to allocate memory for hDisplayActive");
            continue;
        }

        apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
            goto END;
        }

        apiResult = GetActiveDisplay(&displayCount, hDisplayOutput, hDisplayActive, pPanelInfo->targetID);
        if (FALSE == apiResult)
        {
            ERROR_LOG("Failed to get Active Displays during GetTargetDisplayHandle() Call !!!");
            goto END;
        }

        INFO_LOG("GetTargetDisplayHandle() displayCount %d ", displayCount);

        if (NULL == hDisplayActive[displayIndex])
            apiResult = FALSE;
        else
        {
            *htargetDisplay = *hDisplayActive;
        }
    }
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayActive);
    return apiResult;
}

bool ControlAPIGetSetCombinedDisplay(ctl_combined_display_args_t *argsCombinedDisplay, MULTI_PANEL_INFO *pMultiPanelInfo)
{
    bool                         apiResult              = TRUE;
    uint32_t                     adapterIndex           = 0;
    uint32_t                     adapterCount           = 0;
    uint32_t                     displayCount           = 0;
    uint32_t                     displayIndex           = 0;
    uint8_t                      CombinedDisplayCount   = 0;
    ctl_combined_display_args_t  CombinedDisplayArgs    = { 0 };
    ctl_device_adapter_handle_t *hDevices               = nullptr;
    ctl_device_adapter_handle_t *hActDevices            = nullptr;
    ctl_device_adapter_handle_t *hDeviceTest            = nullptr;
    ctl_display_output_handle_t *hDisplayOutput         = nullptr;
    ctl_display_output_handle_t *hDisplayTest           = nullptr;
    ctl_display_output_handle_t *hCombinedDisplayOutput = nullptr;

    INFO_LOG("ControlAPIGetSetCombinedDisplay CAPI called for optype %d and display count %d", argsCombinedDisplay->OpType, argsCombinedDisplay->NumOutputs);
    DEBUG_LOG("Multi Panel Info has display count %d", pMultiPanelInfo->Count);

    if (argsCombinedDisplay->NumOutputs != pMultiPanelInfo->Count)
    {
        ERROR_LOG("Display Count mismatch between CAPI args and Display adaptor info!!");
        return FALSE;
    }

    CombinedDisplayArgs.Size                  = argsCombinedDisplay->Size;
    CombinedDisplayArgs.Version               = argsCombinedDisplay->Version;
    CombinedDisplayArgs.OpType                = argsCombinedDisplay->OpType;
    CombinedDisplayArgs.NumOutputs            = argsCombinedDisplay->NumOutputs;
    CombinedDisplayArgs.CombinedDesktopHeight = argsCombinedDisplay->CombinedDesktopHeight;
    CombinedDisplayArgs.CombinedDesktopWidth  = argsCombinedDisplay->CombinedDesktopWidth;

    // Query Intel adapters list
    VERIFY_API_STATUS(ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices));

    hDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDevices);
    hActDevices = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hActDevices);
    hDeviceTest = (ctl_device_adapter_handle_t *)malloc(sizeof(ctl_device_adapter_handle_t) * adapterCount);
    NULL_PTR_CHECK(hDeviceTest);

    apiResult = ControlApiEnumerateDevices(apiContext.apiHandle, &adapterCount, hDevices);
    if (FALSE == apiResult)
    {
        ERROR_LOG("Control API EnumerateDevice Failed!!");
        goto END;
    }

    DEBUG_LOG("Number of Total Gfx Adapters %d", adapterCount);

    // Compare all detected adaptor data with input adaptor data and then compare all displays in that adaptor with input display data
    // both adaptor and display data come from panel info

    for (displayIndex = 0; displayIndex < pMultiPanelInfo->Count; displayIndex++)
    {

        if (FALSE == GetActiveAdapter(&adapterCount, hDevices, hActDevices, pMultiPanelInfo->panelInfo[displayIndex].gfxAdapter.deviceID))
        {
            ERROR_LOG("Failed to get any Active Adapter for deviceID() %s !!!", pMultiPanelInfo->panelInfo[displayIndex].gfxAdapter.deviceID);
            goto END;
        }

        DEBUG_LOG("Number of Matching Gfx Adapters for Given device ID: %s is Count : %d", pMultiPanelInfo->panelInfo[displayIndex].gfxAdapter.deviceID, adapterCount);

        for (adapterIndex = 0; adapterIndex < adapterCount; adapterIndex++)
        {
            displayCount         = 0;            // reset display count for next iteration
            CombinedDisplayCount = 0;            // reset display count for next iteration
            FREE_MEMORY(hDisplayOutput);         // free memory before each iteration
            FREE_MEMORY(hDisplayTest);           // free memory before each iteration
            FREE_MEMORY(hCombinedDisplayOutput); // free memory before each iteration

            // Enumerate all the possible target displays for the adapters
            VERIFY_API_STATUS(ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput));

            hDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
            NULL_PTR_CHECK(hDisplayOutput);
            hDisplayTest = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
            NULL_PTR_CHECK(hDisplayTest);
            hCombinedDisplayOutput = (ctl_display_output_handle_t *)malloc(sizeof(ctl_display_output_handle_t) * displayCount);
            NULL_PTR_CHECK(hCombinedDisplayOutput);

            apiResult = ControlApiEnumerateDisplayOutputs(hActDevices[adapterIndex], &displayCount, hDisplayOutput);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Control API EnumerateDisplayOutput Failed!!");
                goto END;
            }

            if ((CombinedDisplayArgs.OpType == CTL_COMBINED_DISPLAY_OPTYPE_DISABLE) || (CombinedDisplayArgs.OpType == CTL_COMBINED_DISPLAY_OPTYPE_QUERY_CONFIG))
            {
                for (uint32_t i = 0; i < displayCount; i++)
                {
                    ctl_display_properties_t stDisplayProperties = {};
                    stDisplayProperties.Size                     = sizeof(ctl_display_properties_t);

                    if (NULL == hDisplayOutput[i])
                    {
                        DEBUG_LOG("hDisplayOutput[%d] is NULL.\n", i);
                        goto END;
                    }

                    apiResult = ControlApiGetDisplayProperties(hDisplayOutput[i], &stDisplayProperties);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("Control API ControlApiGetDisplayProperties Failed!!");
                        goto END;
                    }

                    ctl_adapter_display_encoder_properties_t stDisplayEncoderProperties = {};
                    stDisplayEncoderProperties.Size                                     = sizeof(ctl_adapter_display_encoder_properties_t);

                    apiResult = ControlApiGetDisplayEncoderProperties(hDisplayOutput[i], &stDisplayEncoderProperties);
                    if (FALSE == apiResult)
                    {
                        ERROR_LOG("Control API ControlApiGetDisplayEncoderProperties Failed!!");
                        goto END;
                    }

                    // Filter Combined Display output for disable and query operations
                    if (CTL_ENCODER_CONFIG_FLAG_COLLAGE_DISPLAY & stDisplayEncoderProperties.EncoderConfigFlags)
                    {
                        hCombinedDisplayOutput[CombinedDisplayCount++] = hDisplayOutput[i];
                    }
                }

                DEBUG_LOG("CombinedDisplayCount is %d", CombinedDisplayCount);
                CombinedDisplayArgs.hCombinedDisplayOutput = hCombinedDisplayOutput[0]; // Always keeping first display in combined set for removal
            }

            DEBUG_LOG("Enumerated Display Encoder Objects %d for adapter index %d and for multidisplayadaptorindex %d", displayCount, adapterIndex, displayIndex);

            if (displayCount == 0)
            {
                continue;
            }

            DEBUG_LOG("TargetID %d and display count %d", pMultiPanelInfo->panelInfo[displayIndex].targetID, displayCount);
            apiResult = GetDisplayHandle(&displayCount, hDisplayOutput, hDisplayTest, pMultiPanelInfo->panelInfo[displayIndex].targetID);
            if (FALSE == apiResult)
            {
                ERROR_LOG("Failed to get Display Handle for adaptor count %d and for multidisplayadaptorindex %d!!!", adapterIndex, displayIndex);
                goto END;
            }

            hDeviceTest[0]                                               = hActDevices[adapterIndex];
            argsCombinedDisplay->pChildInfo[displayIndex].hDisplayOutput = *hDisplayTest;

            DEBUG_LOG("Display Handle Match With Target ID %d", pMultiPanelInfo->panelInfo[displayIndex].targetID);
        }
    }

    CombinedDisplayArgs.pChildInfo = argsCombinedDisplay->pChildInfo;

    apiResult = ControlAPIGetSetCombinedDisplayEx(*hDeviceTest, &CombinedDisplayArgs);
END:
    FREE_MEMORY(hDevices);
    FREE_MEMORY(hActDevices);
    FREE_MEMORY(hDeviceTest);
    FREE_MEMORY(hDisplayOutput);
    FREE_MEMORY(hDisplayTest);
    FREE_MEMORY(hCombinedDisplayOutput);
    return apiResult;
}
