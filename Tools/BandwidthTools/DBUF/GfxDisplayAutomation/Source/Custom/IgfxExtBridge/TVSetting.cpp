// TVSetting.cpp : Implementation of CTVSetting
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "TVSetting.h"
#include "Guids.h"


ICUIExternal8Ptr CTVSetting::ptrCUIExternal;

CTVSetting::CTVSetting()
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
/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pAvailableConnectors"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::GetAvailableConnectors(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)		
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));

		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		hr = ptrCUIExternal->GetAvailableConnectors(monitorID,pAvailableConnectors,(DWORD *)pExtraErrorCode);
		
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pAvailableConnectors"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>

STDMETHODIMP CTVSetting::GetConnectorSelection(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));

		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		hr = ptrCUIExternal->GetConnectorSelection(monitorID,pAvailableConnectors,(DWORD*)pExtraErrorCode);
		
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pAvailableConnectors"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::GetConnectorAttachedStatus(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pAvailableConnectors,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		hr = ptrCUIExternal->GetConnectorAttachedStatus(monitorID,pAvailableConnectors,(DWORD*)pExtraErrorCode);
		
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="availableConnector"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::SetConnectorSelection(/*[in]*/DWORD monitorID,/*[in]*/DWORD availableConnector,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
	
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		hr = ptrCUIExternal->SetConnectorSelection(monitorID,availableConnector,(DWORD*)pExtraErrorCode);
		
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pTVParamaterData"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::GetTvParameters(/*[/*[in]*/DWORD monitorID,/*[out]*/IGFX_TV_PARAMETER_DATA *pTVParamaterData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		IGFX_TV_PARAMETER_DATA tvParametes = {0};

		hr = ptrCUIExternal->GetTvParameters(monitorID,sizeof(IGFX_TV_PARAMETER_DATA),(BYTE *)&tvParametes,(DWORD*)pExtraErrorCode);
		
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pTVParamaterData"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::SetTvParameters(/*[in]*/DWORD monitorID,/*[in]*/IGFX_TV_PARAMETER_DATA *pTVParamaterData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		hr = ptrCUIExternal->SetTvParameters(monitorID,sizeof(IGFX_TV_PARAMETER_DATA),(BYTE *)pTVParamaterData,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pTVFormat"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::TVTypeStdGet(/*[out]*/IGFX_TV_FORMAT_EX *pTVFormat,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		GUID structGUID = IGFX_TV_FORMAT_GUID_1_0;
		hr = ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_TV_FORMAT_EX),(BYTE*)pTVFormat,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pTVFormat"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::TVTypeStdSet(/*[in]*/IGFX_TV_FORMAT_EX *pTVFormat,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		
		GUID structGUID = IGFX_TV_FORMAT_GUID_1_0;
		hr = ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_TV_FORMAT_EX),(BYTE*)pTVFormat,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="pTVFormat"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::ConnectorStatus(/*[out]*/IGFX_CONNECTOR_STATUS *pConnectorStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		GUID structGUID = IGFX_CONNECTOR_STATUS_GUID_1_0;
	    hr = ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_CONNECTOR_STATUS),(BYTE*)pConnectorStatus,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="pPersistanceStatus"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::GetPersistenceStatus(/*[out]*/DWORD *pPersistanceStatus,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		GUID structGUID = IGFX_DRIVER_PERSISTENCE_ALGO_DISABLE;
		hr = ptrCUIExternal->GetDeviceData(&structGUID,sizeof(DWORD),(BYTE*)pPersistanceStatus,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}



	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::SetPersistenceDisable(/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}

		DWORD dwPersistanceDisable = IGFX_DISABLE_DRIVER_PERSISTENCE;
	
		GUID structGUID = IGFX_DRIVER_PERSISTENCE_ALGO_DISABLE;
		hr = ptrCUIExternal->SetDeviceData(&structGUID,sizeof(DWORD),(BYTE*)&dwPersistanceDisable,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CTVSetting::SetPersistenceEnable(/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
			return hr;
		}
	
		DWORD dwPersistanceEnable = IGFX_ENABLE_DRIVER_PERSISTENCE;
	
		GUID structGUID = IGFX_DRIVER_PERSISTENCE_ALGO_DISABLE;
		hr = ptrCUIExternal->SetDeviceData(&structGUID,sizeof(DWORD),(BYTE*)&dwPersistanceEnable,(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy(); 
	}
	return hr;
}