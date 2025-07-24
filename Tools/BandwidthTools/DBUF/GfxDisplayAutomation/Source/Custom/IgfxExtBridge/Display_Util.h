

/* this ALWAYS GENERATED file contains the definitions for the interfaces */


 /* File created by MIDL compiler version 8.00.0595 */
/* at Mon Jun 15 12:52:02 2015
 */
/* Compiler settings for Display_Util.idl:
    Oicf, W1, Zp8, env=Win32 (32b run), target_arch=X86 8.00.0595 
    protocol : dce , ms_ext, c_ext, robust
    error checks: allocation ref bounds_check enum stub_data 
    VC __declspec() decoration level: 
         __declspec(uuid()), __declspec(selectany), __declspec(novtable)
         DECLSPEC_UUID(), MIDL_INTERFACE()
*/
/* @@MIDL_FILE_HEADING(  ) */

#pragma warning( disable: 4049 )  /* more than 64k source lines */


/* verify that the <rpcndr.h> version is high enough to compile this file*/
#ifndef __REQUIRED_RPCNDR_H_VERSION__
#define __REQUIRED_RPCNDR_H_VERSION__ 475
#endif

#include "rpc.h"
#include "rpcndr.h"

#ifndef __RPCNDR_H_VERSION__
#error this stub requires an updated version of <rpcndr.h>
#endif // __RPCNDR_H_VERSION__

#ifndef COM_NO_WINDOWS_H
#include "windows.h"
#include "ole2.h"
#endif /*COM_NO_WINDOWS_H*/

#ifndef __Display_Util_h__
#define __Display_Util_h__

#if defined(_MSC_VER) && (_MSC_VER >= 1020)
#pragma once
#endif

/* Forward Declarations */ 

#ifndef __IDisplayUtil_FWD_DEFINED__
#define __IDisplayUtil_FWD_DEFINED__
typedef interface IDisplayUtil IDisplayUtil;

#endif 	/* __IDisplayUtil_FWD_DEFINED__ */


/* header files for imported files */
#include "oaidl.h"
#include "ocidl.h"
#include "igfxBridgeUDT.h"

#ifdef __cplusplus
extern "C"{
#endif 


#ifndef __IDisplayUtil_INTERFACE_DEFINED__
#define __IDisplayUtil_INTERFACE_DEFINED__

/* interface IDisplayUtil */
/* [unique][helpstring][dual][uuid][object] */ 


EXTERN_C const IID IID_IDisplayUtil;

#if defined(__cplusplus) && !defined(CINTERFACE)
    
    MIDL_INTERFACE("EA9FB107-8829-4672-B16C-9E5B0EEFDE17")
    IDisplayUtil : public IDispatch
    {
    public:
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetDeviceStatus( 
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out][in] */ DWORD *pDevType,
            /* [out] */ DWORD *pDevStatus,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnumActiveDisplay( 
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD id,
            /* [out] */ DWORD *pMonitorID,
            /* [out] */ DWORD *pDevType,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMonitorID( 
            /* [in] */ BSTR deviceName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SingleDisplaySwitch( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DualDisplayClone( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DualDisplayTwin( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ExtendedDesktop( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnableRotation( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DisableRotation( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IsRotationEnabled( 
            /* [in] */ DWORD monitorID,
            /* [out] */ BOOL *pRotationFlag,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetRotationAngle( 
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pRotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Rotate( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetFullScreen( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetScreenCentered( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnablePortraitPolicy( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DisablePortraitPolicy( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnableLandscapePolicy( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DisableLandscapePolicy( 
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSupportedEvents( 
            /* [in] */ DWORD monitorID,
            DWORD *r_ulSupEvents,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE RegisterEvent( 
            /* [in] */ BSTR eventName,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD eventMask,
            /* [out] */ DWORD *pRegID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE UnRegisterEvent( 
            /* [in] */ DWORD regID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAspectScalingCapabilities( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD dwOperatingMode,
            /* [out] */ DWORD *pAspectScalingCaps,
            /* [out] */ DWORD *pCurrentAspectScalingPreference,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetAspectPreference( 
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD aspectScalingCaps,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetGammaRamp( 
            /* [in] */ DWORD monitorID,
            /* [in] */ GAMMARAMP *pGammaramp,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetGammaRamp( 
            /* [in] */ DWORD uidMonitor,
            /* [out] */ GAMMARAMP *pGammaramp,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE PopulateSetValidGamma( 
            /* [in] */ DWORD monitorID,
            /* [in] */ float gam,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE PopulateSetInvalidGamma( 
            /* [in] */ DWORD monitorID,
            /* [in] */ int rule,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCloneRefreshRate( 
            /* [in] */ DISPLAY_CONFIG *pDispCfg,
            /* [out] */ REFRESHRATE pPrimaryRR[ 20 ],
            /* [out] */ REFRESHRATE pSecondaryRR[ 20 ],
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetCloneView( 
            /* [in] */ DISPLAY_CONFIG *pDispCfg,
            /* [in] */ REFRESHRATE *pPrimaryRR,
            /* [in] */ REFRESHRATE *pSecondaryRR,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetDVMTData( 
            /* [out] */ IGFX_DVMT_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetEDIDData( 
            /* [out][in] */ IGFX_EDID_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IsOverlayOn( 
            /* [out] */ IGFX_OVERLAY_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetOverScanData( 
            /* [out][in] */ IGFX_SCALING_1_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetOverScanData( 
            /* [in] */ IGFX_SCALING_1_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IsDownScalingSupported( 
            /* [in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IsDownScalingEnabled( 
            /* [out] */ int *pbIsEnabled,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnableDownScaling( 
            /* [out][in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DisableDownScaling( 
            /* [out][in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetConfiguration( 
            /* [out][in] */ IGFX_DISPLAY_CONFIG_1_1 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetConfiguration( 
            /* [in] */ IGFX_DISPLAY_CONFIG_1_1 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Overlay_Set( 
            /* [out][in] */ IGFX_OVERLAY_COLOR_SETTINGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE Overlay_Get( 
            /* [out][in] */ IGFX_OVERLAY_COLOR_SETTINGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE CVT_Get( 
            /* [out][in] */ IGFX_FEATURE_SUPPORT_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SDVO_Set( 
            /* [out][in] */ IGFX_VENDOR_OPCODE_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSupportedConfiguration( 
            /* [out][in] */ IGFX_TEST_CONFIG *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetGraphicsModes( 
            /* [out][in] */ IGFX_VIDEO_MODE_LIST *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSupportedGraphicsModes( 
            /* [out][in] */ IGFX_VIDEO_MODE_LIST *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVBIOSVersion( 
            /* [out][in] */ BSTR *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetGammaBrightnessContrast( 
            /* [out][in] */ IGFX_DESKTOP_GAMMA_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetGammaBrightnessContrast( 
            /* [out][in] */ IGFX_DESKTOP_GAMMA_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetSystemConfigurationAll( 
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pSysConfigData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [in] */ DWORD opmode,
            /* [in] */ DWORD PriRotAngle,
            /* [in] */ DWORD SecRotAngle,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetSystemConfiguration( 
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pSysConfigData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSystemConfiguration( 
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetMediaScalar( 
            /* [out][in] */ IGFX_MEDIA_SCALAR *pMediaScalarData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMediaScalar( 
            /* [out][in] */ IGFX_MEDIA_SCALAR *pMediaScalarData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE InitilizeRemoveCustomModeArray( 
            /* [in] */ DWORD monitorId,
            /* [in] */ DWORD i,
            /* [in] */ DWORD HzR,
            /* [in] */ DWORD VtR,
            /* [in] */ DWORD RR,
            /* [in] */ DWORD BPP,
            /* [in] */ DWORD Imode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE RemoveCustomMode( 
            /* [out][in] */ IGFX_CUSTOM_MODELIST *rcm,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE AddAdvancedCustomMode( 
            /* [out][in] */ IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA *pacmd,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE AddBasicCustomMode( 
            /* [out][in] */ IGFX_ADD_BASIC_CUSTOM_MODE_DATA *pbcmd,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCustomModeTiming( 
            /* [out][in] */ IGFX_CUSTOM_MODE_TIMING_DATA *pcmt,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCustomModeList( 
            /* [out][in] */ IGFX_CUSTOM_MODELIST *pCustomerModeList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetMediaScaling( 
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA *pMediaScalingData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMediaScaling( 
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA *pMediaScalingData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetMediaColor( 
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA *pMediaColorData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMediaColor( 
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA *pMediaColorData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetVideoQuality( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA *pVideoQualityData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoQuality( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA *pVideoQualityData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAviInfoFrame( 
            /* [out][in] */ IGFX_AVI_INFOFRAME *pAVIFrameInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetAviInfoFrame( 
            /* [out][in] */ IGFX_AVI_INFOFRAME *pAVIFrameInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAttachedDevices( 
            /* [in] */ OSTYPE osType,
            /* [out] */ DWORD *pAttachedDevices,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnumAttachedDevices( 
            /* [out] */ DWORD *pAttachedDevices,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ChangeActiveDevices( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            DISPLAY_DEVICE_CONFIG_FLAG dwFlags,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DummyFunction( 
            /* [in] */ DISPLAY_RELATED *pDisplayRelated,
            /* [in] */ OPERATING_MODE *pOperatingMode,
            /* [in] */ NEW_DEVICE_TYPE *pDeviceType,
            /* [in] */ DISPLAY_DEVICE_STATUS *pDisplayDeviceStatus,
            /* [in] */ IGFX_DISPLAY_TYPES *pDisplayTypes,
            /* [in] */ GENERIC *pGeneric,
            /* [in] */ IGFX_MEDIA_FEATURE_TYPES *pMediaFeatureTypes,
            /* [in] */ IGFX_COLOR_QUALITIES *pColorQualities,
            /* [in] */ IGFX_TIMING_STANDARDS *pTimingStandards,
            /* [in] */ IGFX_CUSTOM_MODES *pCustomModes,
            /* [in] */ IGFX_DISPLAY_RESOLUTION_EX *Resolution,
            /* [in] */ IGFX_DISPLAY_POSITION *Position,
            REFRESHRATE *pRefreshRate,
            /* [in] */ DISPLAY_CONFIG_CODES *pDisplayConfigCodes,
            /* [in] */ DISPLAY_ORIENTATION *pDisplayOrientation,
            /* [in] */ MEDIA_GAMUT_COMPRESSION_VALUES *pMediaGamutCompressionValues) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCurrentConfig( 
            /* [out][in] */ DEVICE_DISPLAYS *pDeviceDisplays,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IsWOW64( 
            BOOL *pIsWOW64,
            BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DoEscape( 
            /* [in] */ OSTYPE osType,
            /* [in] */ BSTR *pKeyName,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetHueSaturation( 
            /* [out][in] */ IGFX_HUESAT_INFO *pHueSat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetHueSaturation( 
            /* [out][in] */ IGFX_HUESAT_INFO *pHueSat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoQualityExtended( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetVideoQualityExtended( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSystemConfigDataNViews( 
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetSystemConfigDataNViews( 
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetScaling( 
            /* [out][in] */ IGFX_SCALING_2_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetScaling( 
            /* [out][in] */ IGFX_SCALING_2_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE QueryforVideoModeList( 
            /* [out][in] */ IGFX_VIDEO_MODE_LIST_EX *pVideoModeList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetIndividualVideoMode( 
            /* [out][in] */ IGFX_DISPLAY_RESOLUTION_EX *pVideoMode,
            /* [in] */ DWORD index,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetTriClone( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [in] */ DWORD tertiaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetTriExtended( 
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [in] */ DWORD tertiaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetGamutData( 
            /* [out][in] */ IGFX_GAMUT_EXPANSION *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetGamutData( 
            /* [out][in] */ IGFX_GAMUT_EXPANSION *pGamutData,
            /* [in] */ float CSCMatrixRow1[ 3 ],
            /* [in] */ float CSCMatrixRow2[ 3 ],
            /* [in] */ float CSCMatrixRow3[ 3 ],
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCSCData( 
            /* [out][in] */ IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetCSCData( 
            /* [out][in] */ IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoQualityExtended2( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetVideoQualityExtended2( 
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMediaColorExtended2( 
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetMediaColorExtended2( 
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAuxInfo( 
            /* [out][in] */ IGFX_AUX_INFO *pAuxInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetAuxInfo( 
            /* [out][in] */ IGFX_AUX_INFO *pAuxInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSourceHdmiGBDdata( 
            /* [out][in] */ IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetSourceHdmiGBDdata( 
            /* [out][in] */ IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetSupportedConfigurationEx( 
            /* [out][in] */ IGFX_TEST_CONFIG_EX *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetColorGamut( 
            /* [out][in] */ IGFX_GAMUT *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetColorGamut( 
            /* [out][in] */ IGFX_GAMUT *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetXvYcc( 
            /* [out][in] */ IGFX_XVYCC_INFO *pXvyccData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetXvYcc( 
            /* [out][in] */ IGFX_XVYCC_INFO *pXvyccData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetYcBcr( 
            /* [out][in] */ IGFX_YCBCR_INFO *pYCBCRData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetYcBcr( 
            /* [out][in] */ IGFX_YCBCR_INFO *pYCBCRData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetGOPVersion( 
            /* [out][in] */ IGFX_GOP_VERSION *pGopVersion,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoModeListEx( 
            /* [out][in] */ IGFX_VIDEO_MODE_LIST_EX *pVideoModeListEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoGamutMapping( 
            /* [out][in] */ IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetVideoGamutMapping( 
            /* [out][in] */ IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetChipSetInformation( 
            /* [out][in] */ DWORD *pChipsetInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetVideoFeatureSupportList( 
            /* [out][in] */ IGFX_FEATURE_SUPPORT_ARGS *pVideoSupportList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetMediaScalingEx2( 
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetMediaScalingEx2( 
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ReadRegistryEnableNLAS( 
            DWORD *regvalue) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ReadRegistryNLASVerticalCrop( 
            float *regvalue) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ReadRegistryNLASHLinearRegion( 
            float *regvalue) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE ReadRegistryNLASNonLinearCrop( 
            float *regvalue) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnumAttachableDevices( 
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out][in] */ DWORD *pDevType,
            /* [out] */ DWORD *pDevStatus,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetGraphcisRestoreDefault( 
            /* [out][in] */ IGFX_RESTORE_GRAPHICS_DEFAULT_INFO *pGraphicsRestoreDefault,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetDisplayInformation( 
            /* [out][in] */ DWORD *pDisplayInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetIndividualRefreshRate( 
            /* [out][in] */ REFRESHRATE *rr,
            /* [out][in] */ REFRESHRATE refreshrate[ 20 ],
            /* [in] */ DWORD index,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetBusInfo( 
            /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetBusInfo( 
            /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAviInfoFrameEx( 
            /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetAviInfoFrameEx( 
            /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetBezel( 
            /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetBezel( 
            /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetCollageStatus( 
            /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetCollageStatus( 
            /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE SetAudioTopology( 
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE GetAudioTopology( 
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE EnableAudioWTVideo( 
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
        virtual /* [helpstring][id] */ HRESULT STDMETHODCALLTYPE DisableAudioWTVideo( 
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription) = 0;
        
    };
    
    
#else 	/* C style interface */

    typedef struct IDisplayUtilVtbl
    {
        BEGIN_INTERFACE
        
        HRESULT ( STDMETHODCALLTYPE *QueryInterface )( 
            IDisplayUtil * This,
            /* [in] */ REFIID riid,
            /* [annotation][iid_is][out] */ 
            _COM_Outptr_  void **ppvObject);
        
        ULONG ( STDMETHODCALLTYPE *AddRef )( 
            IDisplayUtil * This);
        
        ULONG ( STDMETHODCALLTYPE *Release )( 
            IDisplayUtil * This);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfoCount )( 
            IDisplayUtil * This,
            /* [out] */ UINT *pctinfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetTypeInfo )( 
            IDisplayUtil * This,
            /* [in] */ UINT iTInfo,
            /* [in] */ LCID lcid,
            /* [out] */ ITypeInfo **ppTInfo);
        
        HRESULT ( STDMETHODCALLTYPE *GetIDsOfNames )( 
            IDisplayUtil * This,
            /* [in] */ REFIID riid,
            /* [size_is][in] */ LPOLESTR *rgszNames,
            /* [range][in] */ UINT cNames,
            /* [in] */ LCID lcid,
            /* [size_is][out] */ DISPID *rgDispId);
        
        /* [local] */ HRESULT ( STDMETHODCALLTYPE *Invoke )( 
            IDisplayUtil * This,
            /* [annotation][in] */ 
            _In_  DISPID dispIdMember,
            /* [annotation][in] */ 
            _In_  REFIID riid,
            /* [annotation][in] */ 
            _In_  LCID lcid,
            /* [annotation][in] */ 
            _In_  WORD wFlags,
            /* [annotation][out][in] */ 
            _In_  DISPPARAMS *pDispParams,
            /* [annotation][out] */ 
            _Out_opt_  VARIANT *pVarResult,
            /* [annotation][out] */ 
            _Out_opt_  EXCEPINFO *pExcepInfo,
            /* [annotation][out] */ 
            _Out_opt_  UINT *puArgErr);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetDeviceStatus )( 
            IDisplayUtil * This,
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out][in] */ DWORD *pDevType,
            /* [out] */ DWORD *pDevStatus,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnumActiveDisplay )( 
            IDisplayUtil * This,
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD id,
            /* [out] */ DWORD *pMonitorID,
            /* [out] */ DWORD *pDevType,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMonitorID )( 
            IDisplayUtil * This,
            /* [in] */ BSTR deviceName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SingleDisplaySwitch )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DualDisplayClone )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DualDisplayTwin )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ExtendedDesktop )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnableRotation )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DisableRotation )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *IsRotationEnabled )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ BOOL *pRotationFlag,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetRotationAngle )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ DWORD *pRotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Rotate )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetFullScreen )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetScreenCentered )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnablePortraitPolicy )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DisablePortraitPolicy )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnableLandscapePolicy )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD rotationAngle,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DisableLandscapePolicy )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSupportedEvents )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            DWORD *r_ulSupEvents,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *RegisterEvent )( 
            IDisplayUtil * This,
            /* [in] */ BSTR eventName,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD eventMask,
            /* [out] */ DWORD *pRegID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *UnRegisterEvent )( 
            IDisplayUtil * This,
            /* [in] */ DWORD regID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAspectScalingCapabilities )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD dwOperatingMode,
            /* [out] */ DWORD *pAspectScalingCaps,
            /* [out] */ DWORD *pCurrentAspectScalingPreference,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetAspectPreference )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ DWORD aspectScalingCaps,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetGammaRamp )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ GAMMARAMP *pGammaramp,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetGammaRamp )( 
            IDisplayUtil * This,
            /* [in] */ DWORD uidMonitor,
            /* [out] */ GAMMARAMP *pGammaramp,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *PopulateSetValidGamma )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ float gam,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *PopulateSetInvalidGamma )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorID,
            /* [in] */ int rule,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCloneRefreshRate )( 
            IDisplayUtil * This,
            /* [in] */ DISPLAY_CONFIG *pDispCfg,
            /* [out] */ REFRESHRATE pPrimaryRR[ 20 ],
            /* [out] */ REFRESHRATE pSecondaryRR[ 20 ],
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetCloneView )( 
            IDisplayUtil * This,
            /* [in] */ DISPLAY_CONFIG *pDispCfg,
            /* [in] */ REFRESHRATE *pPrimaryRR,
            /* [in] */ REFRESHRATE *pSecondaryRR,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetDVMTData )( 
            IDisplayUtil * This,
            /* [out] */ IGFX_DVMT_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetEDIDData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_EDID_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *IsOverlayOn )( 
            IDisplayUtil * This,
            /* [out] */ IGFX_OVERLAY_1_0 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetOverScanData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SCALING_1_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetOverScanData )( 
            IDisplayUtil * This,
            /* [in] */ IGFX_SCALING_1_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *IsDownScalingSupported )( 
            IDisplayUtil * This,
            /* [in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *IsDownScalingEnabled )( 
            IDisplayUtil * This,
            /* [out] */ int *pbIsEnabled,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnableDownScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DisableDownScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DOWNSCALING_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetConfiguration )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DISPLAY_CONFIG_1_1 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetConfiguration )( 
            IDisplayUtil * This,
            /* [in] */ IGFX_DISPLAY_CONFIG_1_1 *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Overlay_Set )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_OVERLAY_COLOR_SETTINGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *Overlay_Get )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_OVERLAY_COLOR_SETTINGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *CVT_Get )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_FEATURE_SUPPORT_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SDVO_Set )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VENDOR_OPCODE_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSupportedConfiguration )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_TEST_CONFIG *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetGraphicsModes )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_MODE_LIST *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSupportedGraphicsModes )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_MODE_LIST *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVBIOSVersion )( 
            IDisplayUtil * This,
            /* [out][in] */ BSTR *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetGammaBrightnessContrast )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DESKTOP_GAMMA_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetGammaBrightnessContrast )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DESKTOP_GAMMA_ARGS *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetSystemConfigurationAll )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pSysConfigData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [in] */ DWORD opmode,
            /* [in] */ DWORD PriRotAngle,
            /* [in] */ DWORD SecRotAngle,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetSystemConfiguration )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pSysConfigData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSystemConfiguration )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetMediaScalar )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALAR *pMediaScalarData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMediaScalar )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALAR *pMediaScalarData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *InitilizeRemoveCustomModeArray )( 
            IDisplayUtil * This,
            /* [in] */ DWORD monitorId,
            /* [in] */ DWORD i,
            /* [in] */ DWORD HzR,
            /* [in] */ DWORD VtR,
            /* [in] */ DWORD RR,
            /* [in] */ DWORD BPP,
            /* [in] */ DWORD Imode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *RemoveCustomMode )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_CUSTOM_MODELIST *rcm,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *AddAdvancedCustomMode )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA *pacmd,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *AddBasicCustomMode )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_ADD_BASIC_CUSTOM_MODE_DATA *pbcmd,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCustomModeTiming )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_CUSTOM_MODE_TIMING_DATA *pcmt,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCustomModeList )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_CUSTOM_MODELIST *pCustomerModeList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetMediaScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA *pMediaScalingData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMediaScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA *pMediaScalingData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetMediaColor )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA *pMediaColorData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMediaColor )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA *pMediaColorData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetVideoQuality )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA *pVideoQualityData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoQuality )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA *pVideoQualityData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAviInfoFrame )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AVI_INFOFRAME *pAVIFrameInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetAviInfoFrame )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AVI_INFOFRAME *pAVIFrameInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAttachedDevices )( 
            IDisplayUtil * This,
            /* [in] */ OSTYPE osType,
            /* [out] */ DWORD *pAttachedDevices,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnumAttachedDevices )( 
            IDisplayUtil * This,
            /* [out] */ DWORD *pAttachedDevices,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ChangeActiveDevices )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            DISPLAY_DEVICE_CONFIG_FLAG dwFlags,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DummyFunction )( 
            IDisplayUtil * This,
            /* [in] */ DISPLAY_RELATED *pDisplayRelated,
            /* [in] */ OPERATING_MODE *pOperatingMode,
            /* [in] */ NEW_DEVICE_TYPE *pDeviceType,
            /* [in] */ DISPLAY_DEVICE_STATUS *pDisplayDeviceStatus,
            /* [in] */ IGFX_DISPLAY_TYPES *pDisplayTypes,
            /* [in] */ GENERIC *pGeneric,
            /* [in] */ IGFX_MEDIA_FEATURE_TYPES *pMediaFeatureTypes,
            /* [in] */ IGFX_COLOR_QUALITIES *pColorQualities,
            /* [in] */ IGFX_TIMING_STANDARDS *pTimingStandards,
            /* [in] */ IGFX_CUSTOM_MODES *pCustomModes,
            /* [in] */ IGFX_DISPLAY_RESOLUTION_EX *Resolution,
            /* [in] */ IGFX_DISPLAY_POSITION *Position,
            REFRESHRATE *pRefreshRate,
            /* [in] */ DISPLAY_CONFIG_CODES *pDisplayConfigCodes,
            /* [in] */ DISPLAY_ORIENTATION *pDisplayOrientation,
            /* [in] */ MEDIA_GAMUT_COMPRESSION_VALUES *pMediaGamutCompressionValues);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCurrentConfig )( 
            IDisplayUtil * This,
            /* [out][in] */ DEVICE_DISPLAYS *pDeviceDisplays,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *IsWOW64 )( 
            IDisplayUtil * This,
            BOOL *pIsWOW64,
            BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DoEscape )( 
            IDisplayUtil * This,
            /* [in] */ OSTYPE osType,
            /* [in] */ BSTR *pKeyName,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetHueSaturation )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_HUESAT_INFO *pHueSat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetHueSaturation )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_HUESAT_INFO *pHueSat,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoQualityExtended )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetVideoQualityExtended )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSystemConfigDataNViews )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetSystemConfigDataNViews )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SCALING_2_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetScaling )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SCALING_2_0 *pData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *QueryforVideoModeList )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_MODE_LIST_EX *pVideoModeList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetIndividualVideoMode )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_DISPLAY_RESOLUTION_EX *pVideoMode,
            /* [in] */ DWORD index,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetTriClone )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [in] */ DWORD tertiaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetTriExtended )( 
            IDisplayUtil * This,
            /* [in] */ DWORD primaryMonitorID,
            /* [in] */ DWORD secondaryMonitorID,
            /* [in] */ DWORD tertiaryMonitorID,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetGamutData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_GAMUT_EXPANSION *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetGamutData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_GAMUT_EXPANSION *pGamutData,
            /* [in] */ float CSCMatrixRow1[ 3 ],
            /* [in] */ float CSCMatrixRow2[ 3 ],
            /* [in] */ float CSCMatrixRow3[ 3 ],
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCSCData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetCSCData )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoQualityExtended2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetVideoQualityExtended2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMediaColorExtended2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetMediaColorExtended2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAuxInfo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUX_INFO *pAuxInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetAuxInfo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUX_INFO *pAuxInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSourceHdmiGBDdata )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetSourceHdmiGBDdata )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetSupportedConfigurationEx )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_TEST_CONFIG_EX *pBuffer,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetColorGamut )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_GAMUT *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetColorGamut )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_GAMUT *pGamutData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetXvYcc )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_XVYCC_INFO *pXvyccData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetXvYcc )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_XVYCC_INFO *pXvyccData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetYcBcr )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_YCBCR_INFO *pYCBCRData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetYcBcr )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_YCBCR_INFO *pYCBCRData,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetGOPVersion )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_GOP_VERSION *pGopVersion,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoModeListEx )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_VIDEO_MODE_LIST_EX *pVideoModeListEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoGamutMapping )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetVideoGamutMapping )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetChipSetInformation )( 
            IDisplayUtil * This,
            /* [out][in] */ DWORD *pChipsetInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetVideoFeatureSupportList )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_FEATURE_SUPPORT_ARGS *pVideoSupportList,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetMediaScalingEx2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetMediaScalingEx2 )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ReadRegistryEnableNLAS )( 
            IDisplayUtil * This,
            DWORD *regvalue);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ReadRegistryNLASVerticalCrop )( 
            IDisplayUtil * This,
            float *regvalue);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ReadRegistryNLASHLinearRegion )( 
            IDisplayUtil * This,
            float *regvalue);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *ReadRegistryNLASNonLinearCrop )( 
            IDisplayUtil * This,
            float *regvalue);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnumAttachableDevices )( 
            IDisplayUtil * This,
            /* [in] */ BSTR displayName,
            /* [in] */ DWORD index,
            /* [out] */ DWORD *pMonitorID,
            /* [out][in] */ DWORD *pDevType,
            /* [out] */ DWORD *pDevStatus,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetGraphcisRestoreDefault )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_RESTORE_GRAPHICS_DEFAULT_INFO *pGraphicsRestoreDefault,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetDisplayInformation )( 
            IDisplayUtil * This,
            /* [out][in] */ DWORD *pDisplayInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetIndividualRefreshRate )( 
            IDisplayUtil * This,
            /* [out][in] */ REFRESHRATE *rr,
            /* [out][in] */ REFRESHRATE refreshrate[ 20 ],
            /* [in] */ DWORD index,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetBusInfo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetBusInfo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAviInfoFrameEx )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetAviInfoFrameEx )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetBezel )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetBezel )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetCollageStatus )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetCollageStatus )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *SetAudioTopology )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *GetAudioTopology )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *EnableAudioWTVideo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        /* [helpstring][id] */ HRESULT ( STDMETHODCALLTYPE *DisableAudioWTVideo )( 
            IDisplayUtil * This,
            /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
            /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
            /* [out] */ BSTR *pErrorDescription);
        
        END_INTERFACE
    } IDisplayUtilVtbl;

    interface IDisplayUtil
    {
        CONST_VTBL struct IDisplayUtilVtbl *lpVtbl;
    };

    

#ifdef COBJMACROS


#define IDisplayUtil_QueryInterface(This,riid,ppvObject)	\
    ( (This)->lpVtbl -> QueryInterface(This,riid,ppvObject) ) 

#define IDisplayUtil_AddRef(This)	\
    ( (This)->lpVtbl -> AddRef(This) ) 

#define IDisplayUtil_Release(This)	\
    ( (This)->lpVtbl -> Release(This) ) 


#define IDisplayUtil_GetTypeInfoCount(This,pctinfo)	\
    ( (This)->lpVtbl -> GetTypeInfoCount(This,pctinfo) ) 

#define IDisplayUtil_GetTypeInfo(This,iTInfo,lcid,ppTInfo)	\
    ( (This)->lpVtbl -> GetTypeInfo(This,iTInfo,lcid,ppTInfo) ) 

#define IDisplayUtil_GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId)	\
    ( (This)->lpVtbl -> GetIDsOfNames(This,riid,rgszNames,cNames,lcid,rgDispId) ) 

#define IDisplayUtil_Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr)	\
    ( (This)->lpVtbl -> Invoke(This,dispIdMember,riid,lcid,wFlags,pDispParams,pVarResult,pExcepInfo,puArgErr) ) 


#define IDisplayUtil_GetDeviceStatus(This,displayName,index,pMonitorID,pDevType,pDevStatus,pErrorDescription)	\
    ( (This)->lpVtbl -> GetDeviceStatus(This,displayName,index,pMonitorID,pDevType,pDevStatus,pErrorDescription) ) 

#define IDisplayUtil_EnumActiveDisplay(This,displayName,id,pMonitorID,pDevType,pErrorDescription)	\
    ( (This)->lpVtbl -> EnumActiveDisplay(This,displayName,id,pMonitorID,pDevType,pErrorDescription) ) 

#define IDisplayUtil_GetMonitorID(This,deviceName,index,pMonitorID,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMonitorID(This,deviceName,index,pMonitorID,pErrorDescription) ) 

#define IDisplayUtil_SingleDisplaySwitch(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SingleDisplaySwitch(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DualDisplayClone(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DualDisplayClone(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DualDisplayTwin(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DualDisplayTwin(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_ExtendedDesktop(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> ExtendedDesktop(This,primaryMonitorID,secondaryMonitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_EnableRotation(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> EnableRotation(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DisableRotation(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DisableRotation(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_IsRotationEnabled(This,monitorID,pRotationFlag,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> IsRotationEnabled(This,monitorID,pRotationFlag,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetRotationAngle(This,monitorID,pRotationAngle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetRotationAngle(This,monitorID,pRotationAngle,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_Rotate(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Rotate(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetFullScreen(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetFullScreen(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetScreenCentered(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetScreenCentered(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_EnablePortraitPolicy(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> EnablePortraitPolicy(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DisablePortraitPolicy(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DisablePortraitPolicy(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_EnableLandscapePolicy(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> EnableLandscapePolicy(This,monitorID,rotationAngle,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DisableLandscapePolicy(This,monitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DisableLandscapePolicy(This,monitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSupportedEvents(This,monitorID,r_ulSupEvents,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSupportedEvents(This,monitorID,r_ulSupEvents,pErrorDescription) ) 

#define IDisplayUtil_RegisterEvent(This,eventName,monitorID,eventMask,pRegID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> RegisterEvent(This,eventName,monitorID,eventMask,pRegID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_UnRegisterEvent(This,regID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> UnRegisterEvent(This,regID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAspectScalingCapabilities(This,monitorID,dwOperatingMode,pAspectScalingCaps,pCurrentAspectScalingPreference,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAspectScalingCapabilities(This,monitorID,dwOperatingMode,pAspectScalingCaps,pCurrentAspectScalingPreference,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetAspectPreference(This,monitorID,aspectScalingCaps,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetAspectPreference(This,monitorID,aspectScalingCaps,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetGammaRamp(This,monitorID,pGammaramp,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetGammaRamp(This,monitorID,pGammaramp,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetGammaRamp(This,uidMonitor,pGammaramp,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetGammaRamp(This,uidMonitor,pGammaramp,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_PopulateSetValidGamma(This,monitorID,gam,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> PopulateSetValidGamma(This,monitorID,gam,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_PopulateSetInvalidGamma(This,monitorID,rule,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> PopulateSetInvalidGamma(This,monitorID,rule,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetCloneRefreshRate(This,pDispCfg,pPrimaryRR,pSecondaryRR,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCloneRefreshRate(This,pDispCfg,pPrimaryRR,pSecondaryRR,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetCloneView(This,pDispCfg,pPrimaryRR,pSecondaryRR,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetCloneView(This,pDispCfg,pPrimaryRR,pSecondaryRR,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetDVMTData(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetDVMTData(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetEDIDData(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetEDIDData(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_IsOverlayOn(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> IsOverlayOn(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetOverScanData(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetOverScanData(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetOverScanData(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetOverScanData(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_IsDownScalingSupported(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> IsDownScalingSupported(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_IsDownScalingEnabled(This,pbIsEnabled,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> IsDownScalingEnabled(This,pbIsEnabled,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_EnableDownScaling(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> EnableDownScaling(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DisableDownScaling(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DisableDownScaling(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_Overlay_Set(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Overlay_Set(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_Overlay_Get(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> Overlay_Get(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_CVT_Get(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> CVT_Get(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SDVO_Set(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SDVO_Set(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSupportedConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSupportedConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetGraphicsModes(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetGraphicsModes(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSupportedGraphicsModes(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSupportedGraphicsModes(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVBIOSVersion(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVBIOSVersion(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetGammaBrightnessContrast(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetGammaBrightnessContrast(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetGammaBrightnessContrast(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetGammaBrightnessContrast(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetSystemConfigurationAll(This,pSysConfigData,pExtraErrorCode,opmode,PriRotAngle,SecRotAngle,pErrorDescription)	\
    ( (This)->lpVtbl -> SetSystemConfigurationAll(This,pSysConfigData,pExtraErrorCode,opmode,PriRotAngle,SecRotAngle,pErrorDescription) ) 

#define IDisplayUtil_SetSystemConfiguration(This,pSysConfigData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetSystemConfiguration(This,pSysConfigData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSystemConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSystemConfiguration(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetMediaScalar(This,pMediaScalarData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetMediaScalar(This,pMediaScalarData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetMediaScalar(This,pMediaScalarData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMediaScalar(This,pMediaScalarData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_InitilizeRemoveCustomModeArray(This,monitorId,i,HzR,VtR,RR,BPP,Imode,pErrorDescription)	\
    ( (This)->lpVtbl -> InitilizeRemoveCustomModeArray(This,monitorId,i,HzR,VtR,RR,BPP,Imode,pErrorDescription) ) 

#define IDisplayUtil_RemoveCustomMode(This,rcm,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> RemoveCustomMode(This,rcm,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_AddAdvancedCustomMode(This,pacmd,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> AddAdvancedCustomMode(This,pacmd,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_AddBasicCustomMode(This,pbcmd,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> AddBasicCustomMode(This,pbcmd,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetCustomModeTiming(This,pcmt,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCustomModeTiming(This,pcmt,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetCustomModeList(This,pCustomerModeList,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCustomModeList(This,pCustomerModeList,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetMediaScaling(This,pMediaScalingData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetMediaScaling(This,pMediaScalingData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetMediaScaling(This,pMediaScalingData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMediaScaling(This,pMediaScalingData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetMediaColor(This,pMediaColorData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetMediaColor(This,pMediaColorData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetMediaColor(This,pMediaColorData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMediaColor(This,pMediaColorData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetVideoQuality(This,pVideoQualityData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetVideoQuality(This,pVideoQualityData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoQuality(This,pVideoQualityData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoQuality(This,pVideoQualityData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAviInfoFrame(This,pAVIFrameInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAviInfoFrame(This,pAVIFrameInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetAviInfoFrame(This,pAVIFrameInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetAviInfoFrame(This,pAVIFrameInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAttachedDevices(This,osType,pAttachedDevices,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAttachedDevices(This,osType,pAttachedDevices,pErrorDescription) ) 

#define IDisplayUtil_EnumAttachedDevices(This,pAttachedDevices,pErrorDescription)	\
    ( (This)->lpVtbl -> EnumAttachedDevices(This,pAttachedDevices,pErrorDescription) ) 

#define IDisplayUtil_ChangeActiveDevices(This,primaryMonitorID,secondaryMonitorID,dwFlags,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> ChangeActiveDevices(This,primaryMonitorID,secondaryMonitorID,dwFlags,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DummyFunction(This,pDisplayRelated,pOperatingMode,pDeviceType,pDisplayDeviceStatus,pDisplayTypes,pGeneric,pMediaFeatureTypes,pColorQualities,pTimingStandards,pCustomModes,Resolution,Position,pRefreshRate,pDisplayConfigCodes,pDisplayOrientation,pMediaGamutCompressionValues)	\
    ( (This)->lpVtbl -> DummyFunction(This,pDisplayRelated,pOperatingMode,pDeviceType,pDisplayDeviceStatus,pDisplayTypes,pGeneric,pMediaFeatureTypes,pColorQualities,pTimingStandards,pCustomModes,Resolution,Position,pRefreshRate,pDisplayConfigCodes,pDisplayOrientation,pMediaGamutCompressionValues) ) 

#define IDisplayUtil_GetCurrentConfig(This,pDeviceDisplays,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCurrentConfig(This,pDeviceDisplays,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_IsWOW64(This,pIsWOW64,pErrorDescription)	\
    ( (This)->lpVtbl -> IsWOW64(This,pIsWOW64,pErrorDescription) ) 

#define IDisplayUtil_DoEscape(This,osType,pKeyName,pErrorDescription)	\
    ( (This)->lpVtbl -> DoEscape(This,osType,pKeyName,pErrorDescription) ) 

#define IDisplayUtil_GetHueSaturation(This,pHueSat,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetHueSaturation(This,pHueSat,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetHueSaturation(This,pHueSat,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetHueSaturation(This,pHueSat,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoQualityExtended(This,pVideoQualityEx,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoQualityExtended(This,pVideoQualityEx,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetVideoQualityExtended(This,pVideoQualityEx,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetVideoQualityExtended(This,pVideoQualityEx,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSystemConfigDataNViews(This,dataNView,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSystemConfigDataNViews(This,dataNView,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetSystemConfigDataNViews(This,dataNView,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetSystemConfigDataNViews(This,dataNView,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetScaling(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetScaling(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetScaling(This,pData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetScaling(This,pData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_QueryforVideoModeList(This,pVideoModeList,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> QueryforVideoModeList(This,pVideoModeList,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetIndividualVideoMode(This,pVideoMode,index,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetIndividualVideoMode(This,pVideoMode,index,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetTriClone(This,primaryMonitorID,secondaryMonitorID,tertiaryMonitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetTriClone(This,primaryMonitorID,secondaryMonitorID,tertiaryMonitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetTriExtended(This,primaryMonitorID,secondaryMonitorID,tertiaryMonitorID,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetTriExtended(This,primaryMonitorID,secondaryMonitorID,tertiaryMonitorID,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetGamutData(This,pGamutData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetGamutData(This,pGamutData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetGamutData(This,pGamutData,CSCMatrixRow1,CSCMatrixRow2,CSCMatrixRow3,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetGamutData(This,pGamutData,CSCMatrixRow1,CSCMatrixRow2,CSCMatrixRow3,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetCSCData(This,pCSCData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCSCData(This,pCSCData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetCSCData(This,pCSCData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetCSCData(This,pCSCData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoQualityExtended2(This,pVideoQualityEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoQualityExtended2(This,pVideoQualityEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetVideoQualityExtended2(This,pVideoQualityEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetVideoQualityExtended2(This,pVideoQualityEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetMediaColorExtended2(This,pMediaColorEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMediaColorExtended2(This,pMediaColorEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetMediaColorExtended2(This,pMediaColorEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetMediaColorExtended2(This,pMediaColorEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAuxInfo(This,pAuxInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAuxInfo(This,pAuxInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetAuxInfo(This,pAuxInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetAuxInfo(This,pAuxInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSourceHdmiGBDdata(This,pSourceHdmiGBDData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSourceHdmiGBDdata(This,pSourceHdmiGBDData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetSourceHdmiGBDdata(This,pSourceHdmiGBDData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetSourceHdmiGBDdata(This,pSourceHdmiGBDData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetSupportedConfigurationEx(This,pBuffer,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetSupportedConfigurationEx(This,pBuffer,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetColorGamut(This,pGamutData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetColorGamut(This,pGamutData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetColorGamut(This,pGamutData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetColorGamut(This,pGamutData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetXvYcc(This,pXvyccData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetXvYcc(This,pXvyccData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetXvYcc(This,pXvyccData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetXvYcc(This,pXvyccData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetYcBcr(This,pYCBCRData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetYcBcr(This,pYCBCRData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetYcBcr(This,pYCBCRData,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetYcBcr(This,pYCBCRData,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetGOPVersion(This,pGopVersion,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetGOPVersion(This,pGopVersion,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoModeListEx(This,pVideoModeListEx,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoModeListEx(This,pVideoModeListEx,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoGamutMapping(This,pMediaGamutMapping,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoGamutMapping(This,pMediaGamutMapping,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetVideoGamutMapping(This,pMediaGamutMapping,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetVideoGamutMapping(This,pMediaGamutMapping,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetChipSetInformation(This,pChipsetInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetChipSetInformation(This,pChipsetInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetVideoFeatureSupportList(This,pVideoSupportList,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetVideoFeatureSupportList(This,pVideoSupportList,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetMediaScalingEx2(This,mediaScalingEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetMediaScalingEx2(This,mediaScalingEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetMediaScalingEx2(This,mediaScalingEx2,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetMediaScalingEx2(This,mediaScalingEx2,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_ReadRegistryEnableNLAS(This,regvalue)	\
    ( (This)->lpVtbl -> ReadRegistryEnableNLAS(This,regvalue) ) 

#define IDisplayUtil_ReadRegistryNLASVerticalCrop(This,regvalue)	\
    ( (This)->lpVtbl -> ReadRegistryNLASVerticalCrop(This,regvalue) ) 

#define IDisplayUtil_ReadRegistryNLASHLinearRegion(This,regvalue)	\
    ( (This)->lpVtbl -> ReadRegistryNLASHLinearRegion(This,regvalue) ) 

#define IDisplayUtil_ReadRegistryNLASNonLinearCrop(This,regvalue)	\
    ( (This)->lpVtbl -> ReadRegistryNLASNonLinearCrop(This,regvalue) ) 

#define IDisplayUtil_EnumAttachableDevices(This,displayName,index,pMonitorID,pDevType,pDevStatus,pErrorDescription)	\
    ( (This)->lpVtbl -> EnumAttachableDevices(This,displayName,index,pMonitorID,pDevType,pDevStatus,pErrorDescription) ) 

#define IDisplayUtil_SetGraphcisRestoreDefault(This,pGraphicsRestoreDefault,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetGraphcisRestoreDefault(This,pGraphicsRestoreDefault,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetDisplayInformation(This,pDisplayInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetDisplayInformation(This,pDisplayInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetIndividualRefreshRate(This,rr,refreshrate,index,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetIndividualRefreshRate(This,rr,refreshrate,index,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetBusInfo(This,pBusInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetBusInfo(This,pBusInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetBusInfo(This,pBusInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetBusInfo(This,pBusInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAviInfoFrameEx(This,pAVIFrameInfoEx,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAviInfoFrameEx(This,pAVIFrameInfoEx,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetAviInfoFrameEx(This,pAVIFrameInfoEx,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetAviInfoFrameEx(This,pAVIFrameInfoEx,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetBezel(This,pBezelConfig,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetBezel(This,pBezelConfig,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetBezel(This,pBezelConfig,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetBezel(This,pBezelConfig,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetCollageStatus(This,pCollageStatus,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetCollageStatus(This,pCollageStatus,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetCollageStatus(This,pCollageStatus,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetCollageStatus(This,pCollageStatus,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_SetAudioTopology(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> SetAudioTopology(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_GetAudioTopology(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> GetAudioTopology(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_EnableAudioWTVideo(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> EnableAudioWTVideo(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription) ) 

#define IDisplayUtil_DisableAudioWTVideo(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription)	\
    ( (This)->lpVtbl -> DisableAudioWTVideo(This,pAudioFeatureInfo,pExtraErrorCode,pErrorDescription) ) 

#endif /* COBJMACROS */


#endif 	/* C style interface */



/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetDisplayInformation_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ DWORD *pDisplayInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetDisplayInformation_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetIndividualRefreshRate_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ REFRESHRATE *rr,
    /* [out][in] */ REFRESHRATE refreshrate[ 20 ],
    /* [in] */ DWORD index,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetIndividualRefreshRate_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetBusInfo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetBusInfo_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetBusInfo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BUS_INFO *pBusInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_SetBusInfo_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetAviInfoFrameEx_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetAviInfoFrameEx_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetAviInfoFrameEx_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_SetAviInfoFrameEx_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetBezel_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetBezel_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetBezel_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_BEZEL_CONFIG *pBezelConfig,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_SetBezel_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetCollageStatus_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetCollageStatus_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetCollageStatus_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_COLLAGE_STATUS *pCollageStatus,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_SetCollageStatus_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_SetAudioTopology_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_SetAudioTopology_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_GetAudioTopology_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_GetAudioTopology_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_EnableAudioWTVideo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_EnableAudioWTVideo_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);


/* [helpstring][id] */ HRESULT STDMETHODCALLTYPE IDisplayUtil_DisableAudioWTVideo_Proxy( 
    IDisplayUtil * This,
    /* [out][in] */ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo,
    /* [out] */ IGFX_ERROR_CODES *pExtraErrorCode,
    /* [out] */ BSTR *pErrorDescription);


void __RPC_STUB IDisplayUtil_DisableAudioWTVideo_Stub(
    IRpcStubBuffer *This,
    IRpcChannelBuffer *_pRpcChannelBuffer,
    PRPC_MESSAGE _pRpcMessage,
    DWORD *_pdwStubPhase);



#endif 	/* __IDisplayUtil_INTERFACE_DEFINED__ */


/* Additional Prototypes for ALL interfaces */

unsigned long             __RPC_USER  BSTR_UserSize(     unsigned long *, unsigned long            , BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserMarshal(  unsigned long *, unsigned char *, BSTR * ); 
unsigned char * __RPC_USER  BSTR_UserUnmarshal(unsigned long *, unsigned char *, BSTR * ); 
void                      __RPC_USER  BSTR_UserFree(     unsigned long *, BSTR * ); 

/* end of Additional Prototypes */

#ifdef __cplusplus
}
#endif

#endif


