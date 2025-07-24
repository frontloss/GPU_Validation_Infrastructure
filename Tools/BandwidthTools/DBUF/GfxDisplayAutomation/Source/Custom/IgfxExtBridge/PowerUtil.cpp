// CPowerUtil.cpp : Implementation of PowerUtil
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "PowerUtil.h"
#include "Guids.h"
#include <stdio.h>
#include <tchar.h>
#include <math.h>
#include "UserStructs.h"
//#include "mccsconsts.h"

ICUIExternal8Ptr CPowerUtil::m_ptrCUIExternal;

CPowerUtil::CPowerUtil()
{
	if(m_ptrCUIExternal == NULL)
	{
		HRESULT hr = m_ptrCUIExternal.CreateInstance(CLSID_CUIExternal,NULL);
		if(hr != S_OK)
		{
			//log it
		}
	}
}
	

/// <summary>
/// Purpose    : Implementation of CPowerUtil method Open().
/// </summary>
//* Comments   : This function checks if any of the clients have already      *
//*              successfully opened PowerAPI. If any one has, this method    *
//*              returns a failure.
/// <param name="pHandle"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::PowerApiOpen(/*[out]*/DWORD *pHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr=m_ptrCUIExternal->PowerApiOpen((unsigned int *)pHandle,(DWORD *)pExtraErrorCode);
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
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr; 
}

/// <summary>
/// Purpose    : Implementation of CPowerUtil method Close()
/// </summary>
//* Comments   : This function validates on the handle being passed. If it is *
//*              a valid handle, it unlocks power api and sets a flag to      *
//*              indicate that it is ready to take a new PowerApiOpen().
/// <param name="pHandle"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::PowerApiClose(/*[out]*/DWORD pHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}
		
		hr = m_ptrCUIExternal->PowerApiClose((unsigned int)pHandle,(DWORD *)pExtraErrorCode);
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
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
	//	
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}


	return hr;

 
}

/// <summary>
/// Purpose: Gets Power Conservation Capabilities of the system
//* Comments   : This function validates on the handle being passed. If it is *
//*              a valid handle, it queries the power conservation            *
//*              capabilities and returns them as a bitmask.
/// </summary>
/// <param name="handle"></param>
/// <param name="pCaps"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::GetPowerConsCaps(/*[in]*/DWORD handle,/*[out]*/DWORD *pCaps,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}
			
		hr = m_ptrCUIExternal->GetPowerConsCaps((unsigned int )handle,(unsigned long *)pCaps,(DWORD *)pExtraErrorCode);
		
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

/// <summary>
/// Purpose    : Gets the DFGT Policy information from the driver.
/// </summary>
//* Comments   : This function queries the driver for DFGT policy information *
//*              Possible return values 
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Ac_Dc_Current"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::GetPowerPolicy_DFGT(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD AcDc,/*[in]*/IGFX_DFGT_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID;
 
	//IGFX_DFGT_POLICY_1_0 Policy;
	
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		if(AcDc==0)
		{
				structGUID=IGFX_DFGT_POLICY_GUID_1_0;
		}
		else if(AcDc==1)
		{
			structGUID=IGFX_DFGT_POLICY_GUID_1_1;
		}

		hr= m_ptrCUIExternal->GetPowerPolicy(handle,PolicyID,&structGUID,sizeof(IGFX_DFGT_POLICY_1_0),(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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


/// <summary>
/// Purpose    : Sets the DFGT Policy information from the driver. 
//* Comments   : This function sets DFGT policy information to the driver.    *
/// </summary>
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Ac_Dc_Current"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::SetPowerPolicy_DFGT(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD AcDc,/*[in]*/IGFX_DFGT_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID;
 
	//IGFX_DFGT_POLICY_1_0 Policy;
	
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		if(AcDc==0)
		{
			structGUID=IGFX_DFGT_POLICY_GUID_1_0;
		}
		else if(AcDc==1)
		{
			structGUID=IGFX_DFGT_POLICY_GUID_1_1;
		}

		hr= m_ptrCUIExternal->SetPowerPolicy(handle,PolicyID,&structGUID,sizeof(IGFX_DFGT_POLICY_1_0),(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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


/// <summary>
/// Gets the DPST Policy information from the driver.
/// </summary>
///Comments   : This function queries the driver for DPST policy information
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Policy"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::GetPowerPolicy_DPST(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_DPST_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	GUID structGUID=IGFX_DPST_POLICY_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{	
		int nSize = sizeof(IGFX_DPST_POLICY_1_0);

		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->GetPowerPolicy(handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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


/// <summary>
/// Purpose    :Sets the DPST Policy information to the driver.
/// </summary>
//* Comments   : This function sets DPST policy information to the driver 
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Policy"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::SetPowerPolicy_DPST(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_DPST_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	GUID structGUID;
	CComBSTR errorStr = L"";
	try
	{	
		structGUID=IGFX_DPST_POLICY_GUID_1_0;

		int nSize = sizeof(IGFX_DPST_POLICY_1_0);

		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->SetPowerPolicy(handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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


/// <summary>
/// Purpose: Get the Inverter type and the inverter frequency
/// </summary>
/// <param name="PolicyID"></param>
/// <param name="frequency"></param>
/// <param name="InverterType"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::GetInverterParams(/*[in]*/DWORD PolicyID,/*[in][out]*/IGFX_POWER_PARAMS_0 *powerPolicy,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	GUID guid=IGFX_POWER_PARAMS_1_0;	
	CComBSTR errorStr = L"";
	try
	{	
		int cb = sizeof(IGFX_POWER_PARAMS_0);

		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->GetInverterParams(&guid,PolicyID,cb,(BYTE *)powerPolicy,(DWORD *)pExtraErrorCode);
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
	catch(_com_error& error)
	{
		
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();		
	}

	return hr; 
}


/// <summary>
/// Purpose: Set the inverter frequency on the particular inverter type
/// </summary>
/// <param name="PolicyID"></param>
/// <param name="frequency"></param>
/// <param name="InverterType"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::SetInverterParams(/*[in]*/DWORD PolicyID,/*[in][out]*/IGFX_POWER_PARAMS_0 *powerPolicy,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	GUID guid=IGFX_POWER_PARAMS_1_0;	
	CComBSTR errorStr = L"";
	try
	{	
		
		int cb=sizeof(IGFX_POWER_PARAMS_0);
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->SetInverterParams(&guid,PolicyID,cb,(BYTE *)powerPolicy,(DWORD *)pExtraErrorCode);
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

/// <summary>
/// Purpose    : Sets the policy information for a particular Power policy
/// </summary>
//* Comments   : The function does the following validations.                 *
//*              a. Validation of handle                                      *
//*              b. Validation of Power Policy ID 
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Policy"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::SetPowerPolicyAll(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)		
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}
		
		GUID structGUID = IGFX_FEATURE_CONTROL_GUID_1_0;
		int nSize = sizeof(DWORD);
		hr = m_ptrCUIExternal->SetPowerPolicy(handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr; 
}


/// <summary>
/// Purpose    : Gets the policy information for a particular Power policy 
/// </summary>
/// <param name="handle"></param>
/// <param name="PolicyID"></param>
/// <param name="Policy"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CPowerUtil::GetPowerPolicyAll(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/DWORD *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)		
{
	HRESULT hr=S_OK;
	GUID structGUID;
	IGFX_POWER_PARAMS_0 powerPolicy = {0}; 
	CComBSTR errorStr = L"";
	try
	{	
		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}
		
		structGUID = IGFX_FEATURE_CONTROL_GUID_1_0;
		int nSize = sizeof(DWORD);
		hr = m_ptrCUIExternal->GetPowerPolicy((unsigned int)handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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

STDMETHODIMP CPowerUtil::GetPowerInfo(/*[in,out]*/IGFX_POWER_CONSERVATION_DATA *pData, /*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_POWER_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			if(m_ptrCUIExternal == NULL)
			{
				errorStr = L"m_ptrCUIExternal is null";	
				*pErrorDescription=errorStr.Copy();
				return E_FAIL;
			}

			hr=m_ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_POWER_CONSERVATION_DATA),(BYTE*)pData,(DWORD*)pExtraErrorCode);

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
STDMETHODIMP CPowerUtil::SetPowerInfo(/*[in,out]*/IGFX_POWER_CONSERVATION_DATA *pData, /*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_POWER_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			if(m_ptrCUIExternal == NULL)
			{
				errorStr = L"m_ptrCUIExternal is null";	
				*pErrorDescription=errorStr.Copy();
				return E_FAIL;
			}

			hr=m_ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_POWER_CONSERVATION_DATA),(BYTE*)pData,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CPowerUtil::GetPowerPolicy_ADB(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_ADB_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	GUID structGUID;
	CComBSTR errorStr = L"";
	try
	{	
		structGUID=IGFX_ADB_POLICY_GUID_1_0;

		int nSize = sizeof(IGFX_ADB_POLICY_1_0);

		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->GetPowerPolicy(handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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
STDMETHODIMP CPowerUtil::SetPowerPolicy_ADB(/*[in]*/DWORD handle,/*[out]*/DWORD PolicyID,/*[in]*/IGFX_ADB_POLICY_1_0 *Policy, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	GUID structGUID;
	CComBSTR errorStr = L"";
	try
	{	
		structGUID=IGFX_ADB_POLICY_GUID_1_0;

		int nSize = sizeof(IGFX_ADB_POLICY_1_0);

		//ICUIExternal8Ptr m_ptrCUIExternal(__uuidof(CUIExternal));
		if(m_ptrCUIExternal == NULL)
		{
			errorStr = L"m_ptrCUIExternal is null";	
			*pErrorDescription=errorStr.Copy();
			return E_FAIL;
		}

		hr = m_ptrCUIExternal->SetPowerPolicy(handle,PolicyID,&structGUID,nSize,(BYTE *)Policy,(DWORD *)pExtraErrorCode);
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