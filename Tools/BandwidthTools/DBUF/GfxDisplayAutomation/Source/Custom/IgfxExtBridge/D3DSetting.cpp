// CD3DSetting.cpp : Implementation of D3DSetting
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "D3DSetting.h"
#include "Guids.h"
#include "Common.h"
#include <stdio.h>
#include <tchar.h>
#include <math.h>
#include "UserStructs.h"

ICUIExternal8Ptr CD3DSetting::ptrCUIExternal;

CD3DSetting::CD3DSetting()
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

//This method gets the D3D information

STDMETHODIMP CD3DSetting::GetD3DInfo(/*[in,out]*/ IGFX_D3D_INFO *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_D3D_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_D3D_INFO),(BYTE*)pD3D,(DWORD*)pExtraErrorCode);

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

//This method sets the 3D info
STDMETHODIMP CD3DSetting::SetD3DInfo(/*[in,out]*/ IGFX_D3D_INFO *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_D3D_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_D3D_INFO),(BYTE*)pD3D,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CD3DSetting::GetD3DInfoEx(/*[in,out]*/ IGFX_D3D_INFO_EX *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_D3D_INFO_EX_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_D3D_INFO_EX),(BYTE*)pD3D,(DWORD*)pExtraErrorCode);

			if(SUCCEEDED(hr))
			{
				errorStr = L"S_OK";
				*pErrorDescription=errorStr.Copy();	
			}
			else if(hr == E_FAIL)
			{					
				errorStr = L"E_FAIL";
				*pErrorDescription=errorStr.Copy();				
			}
			else if(hr == E_INVALIDARG)
			{
				errorStr = L"E_INVALIDARG";	
				*pErrorDescription=errorStr.Copy();		
			}
			else
			{				
				_com_error err(hr);
				errorStr = err.ErrorMessage();	
				*pErrorDescription=errorStr.Copy();
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

//This method sets the 3D info
STDMETHODIMP CD3DSetting::SetD3DInfoEx(/*[in,out]*/ IGFX_D3D_INFO_EX *pD3D,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_D3D_INFO_EX_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_D3D_INFO_EX),(BYTE*)pD3D,(DWORD*)pExtraErrorCode);

			if(SUCCEEDED(hr))
			{
				errorStr = L"S_OK";
				*pErrorDescription=errorStr.Copy();	
			}
			else if(hr == E_FAIL)
			{					
				errorStr = L"E_FAIL";
				*pErrorDescription=errorStr.Copy();				
			}
			else if(hr == E_INVALIDARG)
			{
				errorStr = L"E_INVALIDARG";	
				*pErrorDescription=errorStr.Copy();		
			}
			else
			{				
				_com_error err(hr);
				errorStr = err.ErrorMessage();	
				*pErrorDescription=errorStr.Copy();
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
