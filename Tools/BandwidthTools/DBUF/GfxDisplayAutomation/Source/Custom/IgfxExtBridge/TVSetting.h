// TVSetting.h : Declaration of the CTVSetting

#ifndef __TVSETTING_H_
#define __TVSETTING_H_

#include "resource.h"       // main symbols
#import "igfxext.exe" named_guids
using namespace IGFXEXTLib;

/////////////////////////////////////////////////////////////////////////////
// CBridge
class ATL_NO_VTABLE CTVSetting : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CTVSetting, &CLSID_TVSetting>,
	public IDispatchImpl<ITVSetting, &IID_ITVSetting, &LIBID_IGFXEXTBRIDGELib>
{
public:
	CTVSetting();
	//{		
	//}
	static ICUIExternal8Ptr ptrCUIExternal;

DECLARE_REGISTRY_RESOURCEID(IDR_TVSETTING)

DECLARE_PROTECT_FINAL_CONSTRUCT()

BEGIN_COM_MAP(CTVSetting)
	COM_INTERFACE_ENTRY(ITVSetting)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()

	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

	STDMETHOD(GetAvailableConnectors)(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);		
	STDMETHOD(GetConnectorSelection) (/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetConnectorAttachedStatus) (/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetConnectorSelection)(/*[in]*/DWORD monitorID,/*[in]*/DWORD availableConnector,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetTvParameters)(/*[/*[in]*/DWORD monitorID,/*[out]*/IGFX_TV_PARAMETER_DATA *pTVParamaterData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetTvParameters)(/*[in]*/DWORD monitorID,/*[in]*/IGFX_TV_PARAMETER_DATA *pTVParamaterData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(TVTypeStdGet)(/*[out]*/IGFX_TV_FORMAT_EX *pTVFormat,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(TVTypeStdSet)(/*[in]*/IGFX_TV_FORMAT_EX *pTVFormat,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ConnectorStatus)(/*[out]*/IGFX_CONNECTOR_STATUS *pConnectorStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPersistenceStatus)(/*[out]*/DWORD *pPersistanceStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPersistenceDisable)(/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPersistenceEnable)(/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
};


#endif //__TVSETTING_H_