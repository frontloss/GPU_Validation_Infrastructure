// DisplayUtil.h : Declaration of the CDisplayUtil

#ifndef __DISPLAYUTIL_H_
#define __DISPLAYUTIL_H_

#include "resource.h"       // main symbols
#import "igfxext.exe"  named_guids
//#import "igfxdev.dll"

using namespace IGFXEXTLib;
//using namespace IGFXDEVLib;


/////////////////////////////////////////////////////////////////////////////
// CDisplayUtil
class ATL_NO_VTABLE CDisplayUtil : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CDisplayUtil, &CLSID_DisplayUtil>,	 
	public IDispatchImpl<IDisplayUtil, &IID_IDisplayUtil, &LIBID_IGFXEXTBRIDGELib>
{
public:
	STDMETHOD(DoEscape)(/*[in]*/OSTYPE osType,/*[in]*/BSTR *pKeyName,/*[out]*/BSTR *pErrorDescription);	
	STDMETHOD(IsWOW64)(BOOL *pIsWOW64,BSTR *pErrorDescription);
	//STDMETHOD(EnumExtendedDesktopDisplaySettings)(/*[out]*/DISPLAY_MODE *pDisplay1Mode,/*[out]*/DISPLAY_MODE *pDisplay2Mode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCurrentConfig)(/*[in, out]*/DEVICE_DISPLAYS *pDeviceDisplays,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DummyFunction)(/*[in]*/DISPLAY_RELATED *pDisplayRelated,/*[in]*/OPERATING_MODE *pOperatingMode,
		/*[in]*/NEW_DEVICE_TYPE *pDeviceType,/*[in]*/DISPLAY_DEVICE_STATUS *pDisplayDeviceStatus,
		IGFX_DISPLAY_TYPES *pDisplayTypes,GENERIC *pGeneric,IGFX_MEDIA_FEATURE_TYPES *pMediaFeatureTypes,
		IGFX_COLOR_QUALITIES *pColorQualities,IGFX_TIMING_STANDARDS *pTimingStandards,IGFX_CUSTOM_MODES *pCustomModes,IGFX_DISPLAY_RESOLUTION_EX *Resolution,IGFX_DISPLAY_POSITION *Position,REFRESHRATE *pRefreshRate,DISPLAY_CONFIG_CODES *pDisplayConfigCodes,
		DISPLAY_ORIENTATION *pDisplayOrientation, MEDIA_GAMUT_COMPRESSION_VALUES *pMediaGamutCompressionValues);	
	
	
	CDisplayUtil();
	
	//{		
	//}
	static ICUIExternal8Ptr ptrCUIExternal;
	static IGFX_DISPLAY_RESOLUTION_EX *pVideoModes;
	//static IGFX_DISPLAY_CONFIG_DATA_EX *pDispCfg;

DECLARE_REGISTRY_RESOURCEID(IDR_BRIDGE)

DECLARE_PROTECT_FINAL_CONSTRUCT()

BEGIN_COM_MAP(CDisplayUtil)	
	COM_INTERFACE_ENTRY(IDisplayUtil)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()


	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}


	STDMETHOD(GetDeviceStatus)(/*[in]*/BSTR displayName,/*[in]*/DWORD index, /*[out]*/DWORD *pMonitorID,/*[in,out]*/DWORD *pDevType, /*[out]*/DWORD *pDevStatus,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnumAttachableDevices)(/*[in]*/BSTR displayName,/*[in]*/DWORD index, /*[out]*/DWORD *pMonitorID,/*[in,out]*/DWORD *pDevType, /*[out]*/DWORD *pDevStatus,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnumActiveDisplay)(/*[in]*/BSTR displayName,/*[in]*/DWORD index,/*[out]*/DWORD *pMonitorID, /*[out]*/DWORD *pDevType,/*[out]*/BSTR *pErrorDescription);
	//STDMETHOD(GetConfig)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMonitorID)(/*[in]*/BSTR deviceName,/*[in]*/DWORD index,/*[out]*/DWORD *pMonitorID,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SingleDisplaySwitch)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DualDisplayClone)(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DualDisplayTwin)(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ExtendedDesktop)(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnableRotation)(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DisableRotation)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(IsRotationEnabled)(/*[in]*/DWORD monitorID,/*[out]*/ BOOL *pRotationFlag,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetRotationAngle)(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pRotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Rotate)(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetFullScreen)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetScreenCentered)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnablePortraitPolicy)(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DisablePortraitPolicy)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnableLandscapePolicy)(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DisableLandscapePolicy)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSupportedEvents)(/*[in]*/DWORD monitorID, DWORD* r_ulSupEvents,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(RegisterEvent)(/*[in]*/BSTR eventName,/*[in]*/DWORD monitorID,/*[in]*/DWORD eventMask,/*[out]*/DWORD *pRegID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(UnRegisterEvent)(/*[in]*/DWORD regID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetAspectScalingCapabilities)(/*[in]*/DWORD monitorID,/*[in]*/DWORD dwOperatingMode,/*[out]*/DWORD *pAspectScalingCaps,/*[out]*/DWORD *pCurrentAspectScalingPreference,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetAspectPreference)(/*[in]*/DWORD monitorID,/*[in]*/DWORD aspectScalingCaps,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetGammaRamp)(/*[in]*/DWORD monitorID,/*[in]*/GAMMARAMP *pGammaramp,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetGammaRamp)(/*[in]*/DWORD uidMonitor,/*[out]*/GAMMARAMP *pGammaramp,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(PopulateSetValidGamma)(/*[in]*/DWORD monitorID,/*[in]*/float gam,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(PopulateSetInvalidGamma)(/*[in]*/DWORD monitorID,/*[in]*/int rule,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	//STDMETHOD(SetGetGamma)(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCloneRefreshRate)(/*[in]*/DISPLAY_CONFIG *pDispCfg,/*[out]*/ REFRESHRATE pPrimaryRR[20],/*[out]*/ REFRESHRATE pSecondaryRR[20],/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetCloneView)(/*[in]*/DISPLAY_CONFIG *pDispCfg, /*[in]*/REFRESHRATE *pPrimaryRR,/*[in]*/ REFRESHRATE *pSecondaryRR,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetDVMTData)(/*[out]*/IGFX_DVMT_1_0 *pBuffer,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetEDIDData)(/*[out]*/IGFX_EDID_1_0 *pBuffer,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(IsOverlayOn)(/*[out]*/IGFX_OVERLAY_1_0 *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetOverScanData)(/*[out]*/IGFX_SCALING_1_0 *pData,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetOverScanData)(/*[in]*/IGFX_SCALING_1_0 *pData,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(IsDownScalingSupported)(/*[in]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(IsDownScalingEnabled)(/*[out]*/BOOL *pbIsEnabled,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnableDownScaling)(/*[in, out]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DisableDownScaling)(/*[in, out]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);	
	STDMETHOD(GetConfiguration)(/*[in, out]*/IGFX_DISPLAY_CONFIG_1_1 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetConfiguration)(/*[in, out]*/IGFX_DISPLAY_CONFIG_1_1 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Overlay_Set)(/*[in, out]*/IGFX_OVERLAY_COLOR_SETTINGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Overlay_Get)(/*[in, out]*/IGFX_OVERLAY_COLOR_SETTINGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(CVT_Get)(/*[in, out]*/IGFX_FEATURE_SUPPORT_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SDVO_Set)(/*[in, out]*/IGFX_VENDOR_OPCODE_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSupportedConfiguration)(/*[in, out]*/IGFX_TEST_CONFIG *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetGraphicsModes)(/*[in, out]*/IGFX_VIDEO_MODE_LIST *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSupportedGraphicsModes)(/*[in, out]*/IGFX_VIDEO_MODE_LIST *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetVBIOSVersion)(/*[in, out]*/BSTR *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetGammaBrightnessContrast)(/*[in, out]*/IGFX_DESKTOP_GAMMA_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	
	STDMETHOD(SetGammaBrightnessContrast)(/*[in, out]*/IGFX_DESKTOP_GAMMA_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetSystemConfigurationAll)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *pSysConfigData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[in]*/DWORD opmode,/*[in]*/DWORD PriRotAngle,/*[in]*/DWORD SecRotAngle,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetSystemConfiguration)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *pSysConfigData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSystemConfiguration)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetMediaScalar)(/*[in, out]*/IGFX_MEDIA_SCALAR *pMediaScalarData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMediaScalar)(/*[in, out]*/IGFX_MEDIA_SCALAR *pMediaScalarData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(InitilizeRemoveCustomModeArray)(/*[in]*/DWORD monitorId,/*[in]*/DWORD i,/*[in]*/DWORD HzR,/*[in]*/DWORD VtR,/*[in]*/DWORD RR,/*[in]*/DWORD BPP,/*[in]*/DWORD Imode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(RemoveCustomMode)(/*[in]*/IGFX_CUSTOM_MODELIST *rcm,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(AddAdvancedCustomMode)(/*[in, out]*/IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA *pacmd, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(AddBasicCustomMode)(/*[in, out]*/IGFX_ADD_BASIC_CUSTOM_MODE_DATA *pbcmd, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCustomModeTiming)(/*[in, out]*/IGFX_CUSTOM_MODE_TIMING_DATA *pcmt, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCustomModeList)(/*[in, out]*/IGFX_CUSTOM_MODELIST *pCustomerModeList, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetMediaScaling)(/*[in, out]*/IGFX_MEDIA_SCALING_DATA *pMediaScalingData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMediaScaling)(/*[in, out]*/IGFX_MEDIA_SCALING_DATA *pMediaScalingData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetMediaScalingEx2)(/*[in, out]*/IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMediaScalingEx2)(/*[in, out]*/IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetMediaColor)(/*[in, out]*/IGFX_MEDIA_COLOR_DATA *pMediaColorData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMediaColor)(/*[in, out]*/IGFX_MEDIA_COLOR_DATA *pMediaColorData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetVideoQuality)(/*[in, out]*/IGFX_VIDEO_QUALITY_DATA *pVideoQualityData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetVideoQuality)(/*[in, out]*/IGFX_VIDEO_QUALITY_DATA *pVideoQualityData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetAviInfoFrame)(/*[in, out]*/IGFX_AVI_INFOFRAME *pAVIFrameInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetAviInfoFrame)(/*[in, out]*/IGFX_AVI_INFOFRAME *pAVIFrameInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);	
	STDMETHOD(GetAviInfoFrameEx)(/*[in, out]*/IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetAviInfoFrameEx)(/*[in, out]*/IGFX_AVI_INFOFRAME_EX *pAVIFrameInfoEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetSystemConfigDataNView)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pDataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSystemConfigDataNView)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pDataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSystemConfigDataNViews)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetSystemConfigDataNViews)(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetAttachedDevices)(/*[in]*/OSTYPE osType,/*[out]*/DWORD *pAttachedDevices,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnumAttachedDevices)(/*[out]*/DWORD *pAttachedDevices,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ChangeActiveDevices)/*[in]*/(DWORD primaryMonitorID, /*[in]*/DWORD secondaryMonitorID,/*[in]*/ DISPLAY_DEVICE_CONFIG_FLAG dwFlags,/*/out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetHueSaturation)(/*[in,out]*/ IGFX_HUESAT_INFO *pHueSat, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetHueSaturation)(/*[in,out]*/ IGFX_HUESAT_INFO *pHueSat, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetVideoQualityExtended)(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetVideoQualityExtended)(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetScaling)(/*[in,out]*/IGFX_SCALING_2_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetScaling)(/*[in,out]*/IGFX_SCALING_2_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(QueryforVideoModeList)(/*[out]*/IGFX_VIDEO_MODE_LIST_EX *pVideoModeList,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);	
	STDMETHOD(GetIndividualVideoMode)(/*[in,out]*/ IGFX_DISPLAY_RESOLUTION_EX *pVideoMode, DWORD index,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription);
	STDMETHOD(SetTriClone)(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[in]*/ DWORD tertiaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetTriExtended)(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID, DWORD tertiaryMonitorId,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetGamutData)(/*[in, out]*/IGFX_GAMUT_EXPANSION *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetGamutData)(/*[in, out]*/IGFX_GAMUT_EXPANSION *pGamutData, /*[in]*/ float CSCMatrixRow1[3], /*[in]*/ float CSCMatrixRow2[3], /*[in]*/ float CSCMatrixRow3[3],/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCSCData)(/*[in, out]*/IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetCSCData)(/*[in, out]*/IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	HRESULT VistaEscape(int iEsc, int cbIn, void* pIn,/*[out]*/BSTR *pErrorDescription);
	HRESULT ErrorHandler(/*[in]*/BSTR functionName,/*[in]*/HRESULT hr,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetGraphcisRestoreDefault)(/*[in,out]*/IGFX_RESTORE_GRAPHICS_DEFAULT_INFO *pGraphicsRestoreDefault, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetIndividualRefreshRate)(REFRESHRATE *rr, REFRESHRATE refershrate[20], DWORD index, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);


	//Video
	STDMETHOD(GetVideoQualityExtended2)(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetVideoQualityExtended2)(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetMediaColorExtended2)(/*[in,out]*/IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetMediaColorExtended2)(/*[in,out]*/IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetVideoGamutMapping)(/*[in,out]*/IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetVideoGamutMapping)(/*[in,out]*/IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetVideoFeatureSupportList)(/*[in,out]*/IGFX_FEATURE_SUPPORT_ARGS *pVideoSupportList, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);


	STDMETHOD(GetBezel)(/*[in,out]*/ IGFX_BEZEL_CONFIG *pBezelConfig, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetBezel)(/*[in,out]*/ IGFX_BEZEL_CONFIG *pBezelConfig, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);

	STDMETHOD(GetCollageStatus)(/*[in,out]*/ IGFX_COLLAGE_STATUS *pCollageStatus, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetCollageStatus)(/*[in,out]*/ IGFX_COLLAGE_STATUS *pCollageStatus, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);


	STDMETHOD(GetAuxInfo)(/*[in,out]*/IGFX_AUX_INFO *pAuxInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetAuxInfo)(/*[in,out]*/IGFX_AUX_INFO *pAuxInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetBusInfo)(/*[in,out]*/IGFX_BUS_INFO *pBusInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetBusInfo)(/*[in,out]*/IGFX_BUS_INFO *pBusInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetSourceHdmiGBDdata)(/*[in,out]*/IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetSourceHdmiGBDdata)(/*[in,out]*/IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);

	STDMETHOD(GetSupportedConfigurationEx)(/*[in, out]*/IGFX_TEST_CONFIG_EX *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
    STDMETHOD(GetColorGamut)(/*[in, out]*/IGFX_GAMUT *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetColorGamut)(/*[in, out]*/IGFX_GAMUT *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetXvYcc)(/*[in, out]*/IGFX_XVYCC_INFO *pXvyccData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetXvYcc)(/*[in, out]*/IGFX_XVYCC_INFO *pXvyccData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetYcBcr)(/*[in, out]*/IGFX_YCBCR_INFO *pYCBCRData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetYcBcr)(/*[in, out]*/IGFX_YCBCR_INFO *pYCBCRData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetGOPVersion)(/*[in, out]*/IGFX_GOP_VERSION *pGopVersion, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
    
	STDMETHOD(GetVideoModeListEx)(/*[out]*/IGFX_VIDEO_MODE_LIST_EX *pVideoModeListEx,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);	
	
	STDMETHOD(GetChipSetInformation)(/*[in, out]*/DWORD *pChipsetInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetDisplayInformation)(/*[in, out]*/DWORD *pDisplayInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	
	STDMETHOD(ReadRegistryEnableNLAS)(/*[in,out]*/DWORD *regvalue);
	STDMETHOD(ReadRegistryNLASVerticalCrop)(/*[in,out]*/float *regvalue);
	STDMETHOD(ReadRegistryNLASHLinearRegion)(/*[in,out]*/float *regvalue);
	STDMETHOD(ReadRegistryNLASNonLinearCrop)(/*[in,out]*/float *regvalue);

	STDMETHOD(SetAudioTopology)(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetAudioTopology)(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(EnableAudioWTVideo)(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(DisableAudioWTVideo)(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);

	//To Delete
	//STDMETHOD(GetIndividualCfg)(/*[in,out]*/ IGFX_DISPLAY_CONFIG_DATA_EX *pVideoMode, DWORD index,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription);
	 //STDMETHOD(QueryforDispCfg)(/*[in,out]*/ IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pVideoModeList,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription);
//	HRESULT ErrorHandler2(/*[in]*/BSTR functionName,/*[out]*/BSTR *pErrorDescription);

};

#endif //__DISPLAYUTIL_H_
