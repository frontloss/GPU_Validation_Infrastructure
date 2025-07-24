// MCCSUtil.h : Declaration of the CMCCSUtil

#ifndef __MCCSUTIL_H_
#define __MCCSUTIL_H_

#include "resource.h"       // main symbols

#import "igfxext.exe"  named_guids
#import "igfxdev.dll" named_guids

using namespace IGFXEXTLib;
using namespace IGFXDEVLib;

/////////////////////////////////////////////////////////////////////////////
// CBridge
class ATL_NO_VTABLE CMCCSUtil : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CMCCSUtil, &CLSID_MCCSUtil>,
	public IDispatchImpl<IMCCSUtil, &IID_IMCCSUtil, &LIBID_IGFXEXTBRIDGELib>
{
private:
	static UINT mccsUtilHandle;
public:
	CMCCSUtil();
//	~CMCCSUtil();

	//{		
	//}
	static ICUIExternal8Ptr ptrCUIExternal;
	static ICUIDriverPtr ptrCUIDriver;
DECLARE_REGISTRY_RESOURCEID(IDR_MCCSUTIL)

DECLARE_PROTECT_FINAL_CONSTRUCT()

BEGIN_COM_MAP(CMCCSUtil)
	COM_INTERFACE_ENTRY(IMCCSUtil)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()

	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}

	STDMETHOD(Open)(/*[in]*/DWORD monitorID,/*[out]*/DWORD *punHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription); 		
	STDMETHOD(Close)(/*[in]*/DWORD dwHandle,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Max)(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Min)(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ResetControl)(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCurrent)(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetCurrent)(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD r_unSize,/*[in]*/DWORD pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetCapability)(/*[in]*/DWORD monitorID,/*[out]*/BSTR *pCapability,/*[in,out]*/DWORD *pSize,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ParseCapabilityCmds)(/*[in]*/BSTR *pCapabilities,/*[in]*/DWORD *pulCmdArray,/*[out]*/DWORD *pTotalCmds,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(ParseCapabilityVCP)(/*[in]*/BSTR *pCapabilities,/*[in]*/DWORD *pVcpArray,/*[out]*/DWORD *pTotalCmds,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Get)(/*[in,out]*/IGFX_MCCS_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(Set)(/*[in,out]*/IGFX_MCCS_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
};


#endif //__MCCSUTIL_H_