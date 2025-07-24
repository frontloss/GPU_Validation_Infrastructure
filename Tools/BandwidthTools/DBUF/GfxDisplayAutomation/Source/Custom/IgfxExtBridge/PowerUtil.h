// Power.h : Declaration of the IPowerUtil.cpp
#ifndef __POWERUTIL_H_
#define __POWERUTIL_H_

#include "resource.h"       // main symbols

#import "igfxext.exe" named_guids
//#import "igfxdev.dll"

using namespace IGFXEXTLib;

/////////////////////////////////////////////////////////////////////////////
// CPowerUtil
class ATL_NO_VTABLE CPowerUtil : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CPowerUtil, &CLSID_PowerUtil>,
	public IDispatchImpl<IPowerUtil, &IID_IPowerUtil, &LIBID_IGFXEXTBRIDGELib>
{
public:
	CPowerUtil();
	/*CPowerUtil()
	{
		if(m_ptrCUIExternal == NULL)
		{
			m_ptrCUIExternal.CreateInstance(CLSID_CUIExternal,NULL);
		}
	}*/

	static ICUIExternal8Ptr m_ptrCUIExternal;

DECLARE_REGISTRY_RESOURCEID(IDR_POWERUTIL)

DECLARE_PROTECT_FINAL_CONSTRUCT()

BEGIN_COM_MAP(CPowerUtil)
	COM_INTERFACE_ENTRY(IPowerUtil)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()

	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

	STDMETHOD(PowerApiOpen)(/*[out]*/DWORD *punHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(PowerApiClose)(/*[out]*/DWORD punHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerConsCaps)(/*[in]*/DWORD handle,/*[out]*/DWORD *pCaps,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerPolicy_DFGT)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD AcDc,/*[in]*/IGFX_DFGT_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPowerPolicy_DFGT)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD AcDc,/*[in]*/IGFX_DFGT_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerPolicy_DPST)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_DPST_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPowerPolicy_DPST)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_DPST_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetInverterParams)(/*[in]*/DWORD PolicyID,/*[in][out]*/IGFX_POWER_PARAMS_0 *powerPolicy,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetInverterParams)(/*[in]*/DWORD PolicyID,/*[in][out]*/IGFX_POWER_PARAMS_0 *powerPolicy,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerPolicyAll)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPowerPolicyAll)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerInfo)(/*[in,out]*/IGFX_POWER_CONSERVATION_DATA *pData, /*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPowerInfo)(/*[in,out]*/IGFX_POWER_CONSERVATION_DATA *pData, /*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetPowerPolicy_ADB)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_ADB_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetPowerPolicy_ADB)(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_ADB_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
};

#endif //__POWERUTIL_H_
