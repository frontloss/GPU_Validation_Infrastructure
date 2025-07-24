// CSGUtil.cpp : Implementation of SGUtil
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "SGUtil.h"
#include "Guids.h"
#include "Common.h"
#include <stdio.h>
#include <tchar.h>
#include <math.h>
#include "UserStructs.h"

ICUIExternal8Ptr CSGUtil::ptrCUIExternal;

CSGUtil::CSGUtil()
{
	if(ptrCUIExternal == NULL)
	{
		HRESULT hr = ptrCUIExternal.CreateInstance(CLSID_CUIExternal,NULL);
		if(hr != S_OK)
		{
			//log it
		}
	}
}

STDMETHODIMP CSGUtil::GetSGSolutionType(/*[in,out]*/ IGFX_SYSTEM_IGPU_STATUS_STRUCT *pIGPUStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_SYSTEM_IGPU_STATUS_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_IGPU_STATUS_STRUCT),(BYTE*)pIGPUStatus,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{					
				return S_OK;
			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}