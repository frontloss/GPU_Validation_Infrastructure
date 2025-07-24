/*------------------------------------------------------------------------------------------------*
 *
 * @file     CuiSdk.h
 * @brief    This header file contains Implementation of InitializeCUISDK, UninitializeCUISDK,
 *           ConfigureColorAccuracy, GetDesktopGammaColor, SetDesktopGammaColor, GetNarrowGamut,
 *           GetHueSaturation, SetHueSaturation, GetWideGamutExpansion, SetWideGamutExpansion,
 *           IsCollageEnabled, GetCollageInfo, ApplyCollage, GetSupportedConfig,
 *           CollageGetSupportedModes, VerifyMstTopology
 * @author   Sau, Amit; Lakshmanan, Kiran Kumar
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include "CommonInclude.h"
#include "DisplayColorN.h"
#include "DisplayPortN.h"

// Generic Error Codes
#define IGFX_SUCCESS 0x0000
#define IGFX_REGISTRATION_ERROR 0x0001
#define IGFX_INVALID_EVENTHANDLE 0x0002
#define IGFX_INVALID_EVENTMASK 0x0003
#define IGFX_CORRUPT_BUFFER 0x0004
#define IGFX_UNSUPPORTED_GUID 0x0005
#define IGFX_GETCONFIGURATION_ERROR 0x0006
#define IGFX_DEREGISTRATION_ERROR 0x0007
#define IGFX_INVALIDMONITOR_ID 0x0008
#define IGFX_INVALIDCONFIG_FLAG 0x0009
#define IGFX_SETCONFIGATION_ERROR 0x000A

// Error codes for MCCS
#define IGFX_INVALID_MCCS_HANDLE 0x000C
#define IGFX_INVALID_MCCS_CONTROLCODE 0x000D
#define IGFX_INVALID_MCCS_SIZE 0x000E
#define IGFX_MCCS_DRIVER_ERROR 0x000F
#define IGFX_MCCS_DEVICE_ERROR 0x0010
#define IGFX_MCCS_INVALID_MONITOR 0x0011

// Error codes for PowerAPI.
#define IGFX_POWER_API_NOT_SUPPORTED 0x0013
#define IGFX_POWER_API_LOCKED 0x0014
#define IGFX_POWER_API_INVALID_UNLOCK_REQUEST 0x0015
#define IGFX_INVALID_POWER_HANDLE 0x0016
#define IGFX_INVALID_POWER_POLICY 0x0017
#define IGFX_UNSUPPORTED_POWER_POLICY 0x0018
#define IGFX_POWERDEVICE_ERROR 0x0019
#define IGFX_INVALID_DISPLAYID 0x001A

// Error codes for Aspect Scaling
#define IGFX_WRONG_ASPECT_PREFERENCE 0x001B
#define IGFX_INVAILD_OPERATING_MODE 0x001C

// Error codes for Gamma
#define IGFX_INVALID_GAMMA_RAMP 0x001D

// Error codes for TV Connectors
#define IGFX_INVALID_CONNECTOR_SELECTION 0x001E

// Error Code for Get/Set RR RCR
#define IGFX_INVALID_DEVICE_COMBINATION 0x001F
#define IGFX_SETCLONE_FAILED 0x0020
#define IGFX_INVALID_RESOLUTION 0x0021
#define IGFX_INVALID_CONFIGURATION 0x0022

// Error Codes for PWM Frequency
#define IGFX_UNSUPPORTED_INVERTER 0x0023
#define IGFX_BACKLIGHT_PARAMS_INVALID_FREQ 0x0024

// Error Codes for ICUIExternal8
#define IGFX_FAILURE 0x0025

// Error codes for MCCS
#define IGFX_INVALID_INDEX 0x0026

// Error Code for Persistence Data
#define IGFX_INVALID_INPUT 0x0027

// Error Code for Set Configuration
#define IGFX_INCORRECT_RESOLUTION_FORMAT 0x0028
#define IGFX_INVALID_ORIENTATION_COMBINATION 0x0029
#define IGFX_INVALID_ORIENTATION 0x002A

// Error codes for Custom Mode
#define IGFX_INVALID_CUSTOM_MODE 0x002B
#define IGFX_EXISTING_MODE 0x002C
#define IGFX_EXISTING_BASIC_MODE 0x002D
#define IGFX_EXISTING_ADVANCED_MODE 0x002E
#define IGFX_EXCEEDING_BW_LIMITATION 0x002F
#define IGFX_EXISTING_INSUFFICIENT_MEMORY 0x0030

// Error codes for unsupported features
#define IGFX_UNSUPPORTED_FEATURE 0x0031

// Error code for PF2
#define IGFX_PF2_MEDIA_SCALING_NOT_SUPPORTED 0x0032

// Error codes for AVI InfoFrame RCR: 1022131
#define IGFX_INVALID_QUAN_RANGE 0x0033
#define IGFX_INVALID_SCAN_INFO 0x0034

// Error code for I2C/DDC Bus access
#define IGFX_INVALID_BUS_TYPE 0x0035
#define IGFX_INVALID_OPERATION_TYPE 0x0036
#define IGFX_INVALID_BUS_DATA_SIZE 0x0037
#define IGFX_INVALID_BUS_ADDRESS 0x0038
#define IGFX_INVALID_BUS_DEVICE 0x0039
#define IGFX_INVALID_BUS_FLAGS 0x0040

// Error codes for RCR: 1022465
#define IGFX_INVALID_POWER_PLAN 0x0041
#define IGFX_INVALID_POWER_OPERATION 0x0042

// Error codes for AUX API
#define IGFX_INVALID_AUX_DEVICE 0x0043
#define IGFX_INVALID_AUX_ADDRESS 0x0044
#define IGFX_INVALID_AUX_DATA_SIZE 0x0045
#define IGFX_AUX_DEFER 0x0046
#define IGFX_AUX_TIMEOUT 0x0047
#define IGFX_AUX_INCOMPLETE_WRITE 0x0048

// Error codes for PAR: CUI 3.5
#define IGFX_INVALID_PAR_VALUE 0x0049
#define IGFX_NOT_ENOUGH_RESOURCE 0x004A
#define IGFX_NO_S3D_MODE 0x004B

#define IGFX_LAYOUT_ERROR 0x0037

#define IGFX_UNSUPPORTED_VERSION 0x0050
// Error codes for PAR: CUI 3.5
#define IGFX_S3D_ALREADY_IN_USE_BY_ANOTHER_PROCESS 0x004C
#define IGFX_S3D_INVALID_MODE_FORMAT 0x004D
#define IGFX_S3D_INVALID_MONITOR_ID 0x004E
#define IGFX_S3D_DEVICE_NOT_PRIMARY 0x004F
#define IGFX_S3D_INVALID_GPU_MODE 0x0070

// Error Codes for Turbo Overclocking
#define IGFX_INADEQUATE_PRIVILEGES 0x0051

#define IGFX_PWR_INVALID_DISPLAY 0x0052
#define IGFX_PWR_INVALID_PARAMETER 0x0053
#define IGFX_PWR_OPERATION_FAILED 0x0054
#define IGFX_INVALID_MODE 0x0055
#define IGFX_COLLAGE_MODE_NOT_SUPPORTED 0x0056

#ifdef __cplusplus
extern "C"
{
#endif

    // CuiSdk Exposed APIs

    CDLL_EXPORT BOOLEAN InitializeCUISDKN();
    CDLL_EXPORT BOOLEAN UninitializeCUISDKN();

    // DisplayColor Exposed APIs

    CDLL_EXPORT BOOLEAN ConfigureColorAccuracy(_Out_ IGFX_GAMUT *pNarrowGamutInfo);
    CDLL_EXPORT BOOLEAN GetDesktopGammaColor(_Inout_ IGFX_DESKTOP_GAMMA_ARGS *pGetDesktopGamma);
    CDLL_EXPORT BOOLEAN SetDesktopGammaColor(_In_ IGFX_DESKTOP_GAMMA_ARGS *pGetDesktopGamma);
    CDLL_EXPORT BOOLEAN GetNarrowGamut(_Inout_ IGFX_GAMUT *pNarrowGamutInfo);
    CDLL_EXPORT BOOLEAN GetHueSaturation(_Inout_ IGFX_HUESAT_INFO *pHueSatInfo);
    CDLL_EXPORT BOOLEAN SetHueSaturation(_In_ IGFX_HUESAT_INFO *pHueSatInfo);
    CDLL_EXPORT BOOLEAN GetWideGamutExpansion(_Inout_ IGFX_GAMUT_EXPANSION *pWideGamut);
    CDLL_EXPORT BOOLEAN SetWideGamutExpansion(_In_ IGFX_GAMUT_EXPANSION *pWideGamut);

    // DisplayPort Exposed APIs

    CDLL_EXPORT BOOLEAN IsCollageEnabled(_Inout_ IGFX_COLLAGE_STATUS *pCollageStatus);
    CDLL_EXPORT BOOLEAN GetCollageInfo(_Out_ IGFX_COLLAGE_STATUS *pCollageStatus);
    CDLL_EXPORT BOOLEAN ApplyCollage(_In_ IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pSystemConfigData);
    CDLL_EXPORT BOOLEAN GetSupportedConfig(_In_ IGFX_TEST_CONFIG_EX *pTestConfigEx);
    CDLL_EXPORT BOOLEAN CollageGetSupportedModes(_In_ DWORD size, _Inout_ IGFX_VIDEO_MODE_LIST_EX *pVideoModeList);
    CDLL_EXPORT BOOLEAN VerifyMstTopology(_In_ ULONG portNum);

#ifdef __cplusplus
}
#endif
