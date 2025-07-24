// D3DSetting.h : Declaration of the ID3DSetting.cpp
#ifndef __D3DSETTING_H_
#define __D3DSETTING_H_

#include "resource.h"       // main symbols

#import "igfxext.exe" named_guids
//#import "igfxdev.dll"

using namespace IGFXEXTLib;

/////////////////////////////////////////////////////////////////////////////
// CD3DSetting
class ATL_NO_VTABLE CD3DSetting : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CD3DSetting, &CLSID_D3DSetting>,
	public IDispatchImpl<ID3DSetting, &IID_ID3DSetting, &LIBID_IGFXEXTBRIDGELib>
{
public:
	CD3DSetting();
	static ICUIExternal8Ptr ptrCUIExternal;
DECLARE_REGISTRY_RESOURCEID(IDR_D3DSETTING)

DECLARE_PROTECT_FINAL_CONSTRUCT()

BEGIN_COM_MAP(CD3DSetting)
	COM_INTERFACE_ENTRY(ID3DSetting)
	COM_INTERFACE_ENTRY(IDispatch)
END_COM_MAP()

	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}
	STDMETHOD(GetD3DInfo)(/*[in,out]*/ IGFX_D3D_INFO *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetD3DInfo)(/*[in,out]*/ IGFX_D3D_INFO *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(GetD3DInfoEx)(/*[in,out]*/ IGFX_D3D_INFO_EX *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
	STDMETHOD(SetD3DInfoEx)(/*[in,out]*/ IGFX_D3D_INFO_EX *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
};
#endif //end of _D3DSETTING_H