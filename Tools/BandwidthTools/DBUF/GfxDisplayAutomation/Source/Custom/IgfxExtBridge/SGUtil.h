// SGUtil.h : Declaration of the ISGUtil.cpp
#ifndef __SGUTIL_H_
#define __SGUTIL_H_

#include "resource.h"       // main symbols

#import "igfxext.exe" named_guids
//#import "igfxdev.dll"

using namespace IGFXEXTLib;

/////////////////////////////////////////////////////////////////////////////
// CSGUtil
class ATL_NO_VTABLE CSGUtil : 
	public CComObjectRootEx<CComSingleThreadModel>,
	public CComCoClass<CSGUtil, &CLSID_SGUtil>,
	public IDispatchImpl<ISGUtil, &IID_ISGUtil, &LIBID_IGFXEXTBRIDGELib>
{
	public:
	CSGUtil();
	static ICUIExternal8Ptr ptrCUIExternal;

	DECLARE_REGISTRY_RESOURCEID(IDR_SGUTIL)

	DECLARE_PROTECT_FINAL_CONSTRUCT()

	BEGIN_COM_MAP(CSGUtil)
	COM_INTERFACE_ENTRY(ISGUtil)
	COM_INTERFACE_ENTRY(IDispatch)
	END_COM_MAP()

	STDMETHOD( FinalConstruct())
	{
		return S_OK;
	}

	void FinalRelease()
	{
	}
	STDMETHOD(GetSGSolutionType) (/*[in,out]*/ IGFX_SYSTEM_IGPU_STATUS_STRUCT *pIGPUStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription);
};
#endif //__SGUTIL_H_
