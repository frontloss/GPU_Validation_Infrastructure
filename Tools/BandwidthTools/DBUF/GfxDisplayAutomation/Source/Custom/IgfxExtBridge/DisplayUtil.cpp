// Bridge.cpp : Implementation of CBridge
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "Common.h"
#include "DisplayUtil.h"
#include "Guids.h"
#include <stdio.h>
#include <tchar.h>
#include <math.h>
#include <windows.h>

#include "VistaEscapeCalls.h"
#include "XPEscapeCalls.h"



typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS) (HANDLE, PBOOL);
LPFN_ISWOW64PROCESS fnIsWow64Process;


ICUIExternal8Ptr CDisplayUtil::ptrCUIExternal;

IGFX_DISPLAY_RESOLUTION_EX* CDisplayUtil:: pVideoModes;
//IGFX_DISPLAY_CONFIG_DATA_EX* CDisplayUtil::pDispCfg;

CDisplayUtil::CDisplayUtil()
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
/// This function gets the device status for a given display name and index
/// </summary>
/// <param name="displayName"></param>
/// <param name="index"></param>
/// <param name="pDevType"></param>
/// <param name="pDevStatus"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetDeviceStatus(/*[in]*/BSTR displayName,/*[in]*/DWORD index, /*[out]*/DWORD *pMonitorID,/*[in,out]*/DWORD *pDevType, /*[out]*/DWORD *pDevStatus,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";	

	try
	{ 
	 		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//
			return hr;
		}
	

		for(DWORD counter = 0; counter <= index; ++counter)
		{
			*pMonitorID = 0;
			*pDevStatus = 0;
			*pDevType = IGFX_FLAG_HDMI_DEIVCE_SUPPORT | IGFX_FLAG_NIVO_DEIVCE_SUPPORT | IGFX_FLAG_DP_DEVICE_SUPPORT ;
		
			hr = ptrCUIExternal->EnumAttachableDevices(displayName,counter,pMonitorID,pDevType,pDevStatus);
			if(FAILED(hr))
			{ 
				ErrorHandler(L"GetConfiguration",hr,pErrorDescription); 				
				return S_OK;
			}

			if(hr != S_OK)
			{
				//send the result back to clients				
				return hr;
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
	}

	return hr;
}



STDMETHODIMP CDisplayUtil::EnumAttachableDevices(/*[in]*/BSTR displayName,/*[in]*/DWORD index, /*[out]*/DWORD *pMonitorID,/*[in,out]*/DWORD *pDevType, /*[out]*/DWORD *pDevStatus,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";	

	try
	{ 
		if(ptrCUIExternal == NULL)
		{
			//
			return hr;
		}

		*pMonitorID = 0;
		*pDevStatus = 0;
		*pDevType = IGFX_FLAG_HDMI_DEIVCE_SUPPORT | IGFX_FLAG_NIVO_DEIVCE_SUPPORT | IGFX_FLAG_DP_DEVICE_SUPPORT ;
		
		hr = ptrCUIExternal->EnumAttachableDevices(displayName,index,pMonitorID,pDevType,pDevStatus);
		
		if(FAILED(hr))
		{ 
			ErrorHandler(L"EnumAttachableDevices",hr,pErrorDescription); 				
			return S_OK;
		}

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
/// Gets the active display's monitor ID for a given display name and index
/// </summary>
/// <param name="displayName"></param>
/// <param name="index"></param>
/// <param name="pMonitorID"></param>
/// <param name="pDevType"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::EnumActiveDisplay(/*[in]*/BSTR displayName,/*[in]*/DWORD index, /*[out]*/DWORD *pMonitorID,/*[out]*/DWORD *pDevType,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		*pDevType = 0;
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal)); 
		if(ptrCUIExternal == NULL)
		{
			//
			return hr;
		}
		
		DWORD monitorID = 0;
		DWORD devType = 0;
		
		hr = ptrCUIExternal->EnumActiveDevices(displayName,index,pMonitorID,pDevType);
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
 ///  Retreive the configuration
 /// </summary>
 /// <param name="pBuffer"></param>
 /// <param name="pExtraErrorCode"></param>
 /// <param name="pErrorDescription"></param>
 /// <returns></returns>
STDMETHODIMP CDisplayUtil::GetConfiguration(/*[in, out]*/IGFX_DISPLAY_CONFIG_1_1 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	GUID structGUID=IGFX_DISPLAY_CONFIG_GUID_1_1;

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}	
		
		hr = ptrCUIExternal->GetConfiguration(&structGUID,sizeof(IGFX_DISPLAY_CONFIG_1_1),
						(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);
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
/// 
/// </summary>
/// <param name="deviceName"></param>
/// <param name="index"></param>
/// <param name="pMonitorID"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetMonitorID(/*[in]*/BSTR deviceName,/*[in]*/DWORD index,/*[out]*/DWORD *pMonitorID,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		DWORD dwDeviceType;
		dwDeviceType = IGFX_FLAG_HDMI_DEIVCE_SUPPORT | IGFX_FLAG_NIVO_DEIVCE_SUPPORT;

		DWORD dwStatus=0;		
		hr = GetDeviceStatus(deviceName,index,pMonitorID,&dwDeviceType,&dwStatus,pErrorDescription);
		if(hr != S_OK)
		{
			//throw error
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
/// 
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="dwFlags"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::ChangeActiveDevices(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[in]*/ DISPLAY_DEVICE_CONFIG_FLAG dwFlags,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_DEVICE_DISPLAYS_GUID_1_0;
	
	try
	{
		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		
		DEVICE_DISPLAYS deviceDisplays={0};
		
		deviceDisplays.nSize = sizeof(DEVICE_DISPLAYS);//size of the display device structure
		deviceDisplays.dwFlags = (DWORD)dwFlags;//single display switch
		deviceDisplays.nMonitors = 1;//no of monitors
		deviceDisplays.monitorIDs[0] = secondaryMonitorID;
		lstrcpyW(deviceDisplays.strDeviceName,L"\\\\.\\Display1");   //lstrcpy((TCHAR *)deviceDisplays.strDeviceName,_T("\\\\.\\Display1"));
		deviceDisplays.primaryMonitorID = primaryMonitorID;

		//change the display to given display device
		hr = ptrCUIExternal->ChangeActiveDevices(&structGUID,sizeof(DEVICE_DISPLAYS),(BYTE *)&deviceDisplays,(DWORD*)pExtraErrorCode);
		if(FAILED(hr))
		{
			errorStr = L"E_FAIL";
			*pErrorDescription=errorStr.Copy();
			return S_OK;
		}

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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SingleDisplaySwitch(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		hr = ChangeActiveDevices(0,monitorID,IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE,pExtraErrorCode,pErrorDescription);
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
/// 
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::DualDisplayClone(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		hr = ChangeActiveDevices(primaryMonitorID,secondaryMonitorID,IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE,pExtraErrorCode,pErrorDescription);
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
/// 
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::DualDisplayTwin(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		hr = ChangeActiveDevices(secondaryMonitorID,primaryMonitorID,IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDTWIN,pExtraErrorCode,pErrorDescription);
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
/// 
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::ExtendedDesktop(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_DEVICE_DISPLAYS_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{
		HRESULT hr=S_OK;

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		DEVICE_DISPLAYS aobjDisp[2] = {0};
		
		for(int nIdx=0 ; nIdx < sizeof(aobjDisp)/sizeof(DEVICE_DISPLAYS) ; nIdx++)
		{
			aobjDisp[nIdx].nSize = sizeof(DEVICE_DISPLAYS);
			aobjDisp[nIdx].nMonitors = 1;
			aobjDisp[nIdx].dwFlags = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE;
			aobjDisp[nIdx].primaryMonitorID = 0;
		}
		
		aobjDisp[0].monitorIDs[0] = primaryMonitorID;//primary device
		lstrcpyW(aobjDisp[0].strDeviceName,L"\\\\.\\Display1");  //lstrcpy((TCHAR *)aobjDisp[0].strDeviceName,_T("\\\\.\\Display1"));
		aobjDisp[1].monitorIDs[0] = secondaryMonitorID;//secondary display device
		lstrcpyW(aobjDisp[1].strDeviceName, L"\\\\.\\Display2");  //lstrcpy((TCHAR *)aobjDisp[1].strDeviceName,_T("\\\\.\\Display2"));
		
		//set the extended mode
		hr = ptrCUIExternal->ChangeActiveDevices(&structGUID,2*sizeof(DEVICE_DISPLAYS),(BYTE *)aobjDisp,(DWORD *)pExtraErrorCode);

		if(FAILED(hr))
		{
			errorStr = L"E_FAIL";
			*pErrorDescription=errorStr.Copy();
			return S_OK;
		}

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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="rotationAngle"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::EnableRotation(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bRotationEnabled = true;
			displayConfig.dwOrientation = rotationAngle;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::DisableRotation(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		UINT nIndex = 0;
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bRotationEnabled = false;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pRotationFlag"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::IsRotationEnabled(/*[in]*/DWORD monitorID,/*[out]*/BOOL *pRotationFlag,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		UINT nIndex = 0;
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{
			*pRotationFlag = displayConfig.bRotationEnabled;	
		}
		else
		{
			return S_OK;
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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pRotationAngle"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetRotationAngle(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pRotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		UINT nIndex = 0;
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{
			*pRotationAngle = displayConfig.dwOrientation;	
		}
		else
		{
			return S_OK;
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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="rotationAngle"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::Rotate(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		UINT nIndex = 0;
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{
			switch (rotationAngle)
			{
				case 90:
						displayConfig.dwOrientation = IGFX_DISPLAY_ORIENTATION_90;
						break;
				case 180:
						displayConfig.dwOrientation = IGFX_DISPLAY_ORIENTATION_180;
						break;
				case 270:
						displayConfig.dwOrientation = IGFX_DISPLAY_ORIENTATION_270;
						break;
				default :
						displayConfig.dwOrientation = rotationAngle;
			}

				//displayConfig.dwOrientation = ulRotationAngle;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetFullScreen(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_DISPLAY_CONFIG_GUID_1_1;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		IGFX_DISPLAY_CONFIG_1_1 displayConfig ={0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		displayConfig.lHorizontalScaling = 1;
		displayConfig.lVerticalScaling = 1;
		displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_HORIZONTAL_SCALING | IGFX_DISPLAY_CONFIG_FLAG_VERTICAL_SCALING;

		hr = ptrCUIExternal->SetConfiguration(&structGUID, 
												sizeof(IGFX_DISPLAY_CONFIG_1_1),
												(BYTE*)&displayConfig,
												(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetScreenCentered(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_DISPLAY_CONFIG_GUID_1_1;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		
		IGFX_DISPLAY_CONFIG_1_1 displayConfig ={0};

		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		displayConfig.lHorizontalScaling = 0;
		displayConfig.lVerticalScaling = 0;
		displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_HORIZONTAL_SCALING | IGFX_DISPLAY_CONFIG_FLAG_VERTICAL_SCALING;

		hr = ptrCUIExternal->SetConfiguration(&structGUID, 
												sizeof(IGFX_DISPLAY_CONFIG_1_1),
												(BYTE*)&displayConfig,
												(DWORD*)pExtraErrorCode);
		if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
		{
			return S_OK;
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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="rotationAngle"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::EnablePortraitPolicy(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bPortraitPolicy = true;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ROTATION_PORTRAIT;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::DisablePortraitPolicy(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bPortraitPolicy = false;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ROTATION_PORTRAIT;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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

/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="rotationAngle"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::EnableLandscapePolicy(/*[in]*/DWORD monitorID,/*[in]*/DWORD rotationAngle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};
		displayConfig.uidMonitor = monitorID;
		displayConfig.nSize = sizeof(displayConfig);
		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bLandscapePolicy = true;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ROTATION_LANDSCAPE;
			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::DisableLandscapePolicy(/*[in]*/DWORD monitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;   	
	UINT nIndex = 0;
	CComBSTR errorStr = L"";

	try
	{
		//TODO Implement code here
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	 	
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

	
		IGFX_DISPLAY_CONFIG_1_1 displayConfig = {0};		

		displayConfig.uidMonitor =  monitorID;
		displayConfig.nSize = sizeof(displayConfig);			

		hr = GetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);

		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{	
			displayConfig.bLandscapePolicy = false;
			displayConfig.dwFlags = IGFX_DISPLAY_CONFIG_FLAG_ROTATION_LANDSCAPE;

			hr = SetConfiguration(&displayConfig,pExtraErrorCode,pErrorDescription);
			if(FAILED(hr) || *pExtraErrorCode != IGFX_SUCCESS)
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


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pSupEvents"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetSupportedEvents(/*[in]*/DWORD monitorID, DWORD *pSupEvents,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;    
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			//
			return hr;
		}


		hr = ptrCUIExternal->get_SupportedEvents(monitorID,pSupEvents);

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
//		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
//		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="eventName"></param>
/// <param name="monitorID"></param>
/// <param name="eventMask"></param>
/// <param name="pRegID"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::RegisterEvent(/*[in]*/BSTR eventName,/*[in]*/DWORD monitorID,/*[in]*/DWORD eventMask,/*[out]*/DWORD *pRegID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	unsigned int intRegID;
	CComBSTR errorStr = L"";
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		hr = ptrCUIExternal->RegisterEvent(eventName,monitorID,eventMask,&intRegID,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{		
			return S_OK;	
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
/// 
/// </summary>
/// <param name="regID"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::UnRegisterEvent(/*[in]*/DWORD regID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK; 
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		hr = ptrCUIExternal->DeRegisterEvent(regID,(DWORD*)pExtraErrorCode);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{
			return S_OK;	
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
/// Purpose: This API will get the aspect scaling capabilities and the current aspect scaling preference of a display device
/// </summary>
/// <param name="monitorID"></param>
/// <param name="dwOperatingMode"></param>
/// <param name="pAspectScalingCaps"></param>
/// <param name="pCurrentAspectScalingPreference"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetAspectScalingCapabilities(/*[in]*/DWORD monitorID,/*[in]*/DWORD dwOperatingMode,/*[out]*/DWORD *pAspectScalingCaps,/*[out]*/DWORD *pCurrentAspectScalingPreference,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	
	try
	{
		//monitorID = 1;
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetAspectScalingCapabilities(monitorID,dwOperatingMode,pAspectScalingCaps,pCurrentAspectScalingPreference,(DWORD*)pExtraErrorCode);		

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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="aspectScalingCaps"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetAspectPreference(/*[in]*/DWORD monitorID,/*[in]*/DWORD aspectScalingCaps,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{	
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
 
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

	    hr=ptrCUIExternal->SetAspectScalingPreference(monitorID,aspectScalingCaps,(DWORD*)pExtraErrorCode);
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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pGammaramp"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetGammaRamp(/*[in]*/DWORD monitorID,/*[in]*/GAMMARAMP *pGammaramp,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;	
	CComBSTR errorStr = L"";
  
	try
	{
		int nSize=sizeof(GAMMARAMP);	
	
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		 
		hr=ptrCUIExternal->SetGammaRamp(monitorID,nSize,(BYTE*)pGammaramp,(DWORD*)pExtraErrorCode);
 
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
/// 
/// </summary>
/// <param name="uidMonitor"></param>
/// <param name="pGammaramp"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetGammaRamp(/*[in]*/DWORD uidMonitor,/*[out]*/GAMMARAMP *pGammaramp,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)

{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
 
	try
	{
		//Changes done in LATEST GTA
		
		 GAMMARAMP gammaramp;

		int nSize=sizeof(gammaramp);
		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetGammaRamp(uidMonitor,nSize,(BYTE *)pGammaramp,(DWORD*)pExtraErrorCode);

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
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="gam"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::PopulateSetValidGamma(/*[in]*/DWORD monitorID,/*[in]*/float gam,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK; 
	GAMMARAMP pGammaRamp={0};
	WORD val;
	double corr,og;
	CComBSTR errorStr = L"";
	
	try
	{
		og=0.1 /(gam + 0.00001);	
		corr=255.0 * pow((double) (1.0/255.0),og);
		
		for(int index=0;index<256;index++)
		{
			val=(unsigned short)(corr * pow ((double)(index),og));
			//	pGammaRamp.Red[i]=pGammaRamp.Green[i]=pGammaRamp.Blue[i]=val
			pGammaRamp.Red[index]=pGammaRamp.Green[index]=pGammaRamp.Blue[index]=val*256;
		}

		hr=SetGammaRamp(monitorID,&pGammaRamp,pExtraErrorCode,pErrorDescription);

		if (SUCCEEDED(hr))
		{
			return S_OK ;
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="monitorID"></param>
/// <param name="rule"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::PopulateSetInvalidGamma(/*[in]*/DWORD monitorID,/*[in]*/int rule,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK; 
	GAMMARAMP pGammaRamp={0};
 	int index=0;
	CComBSTR errorStr = L"";
   
	try
	{
		switch(rule)
		{
			case 1:
		 		for(index=0;index<256;index++)
				{
					pGammaRamp.Red[index]=256-index;
					pGammaRamp.Blue[index]=512-index;
					pGammaRamp.Green[index]=1024-index;
				}
				break;

			case 2:  
				for(index=0;index<=50;index++)
				{
					pGammaRamp.Red[index]=0;
					pGammaRamp.Blue[index]=0;
					pGammaRamp.Green[index]=0;
				}
				for(index=51;index<256;index++)
				{
					pGammaRamp.Red[index]=index;
					pGammaRamp.Blue[index]=index;
					pGammaRamp.Green[index]=index;
				}
				break;
			
			case 3:
			  //prindexntf(" \n 176th element indexs same as  256th ");
				for(index=0;index<256;index++)
				{
					pGammaRamp.Red[index]=index;
					pGammaRamp.Blue[index]=512+index;
					pGammaRamp.Green[index]=1024+index;
				}
				 //  Settindexng 176th and 256th element 
				for(index=175;index<256;index++)
				{
					pGammaRamp.Red[index]=200; // Some randon values 
					pGammaRamp.Blue[index]=20000;
					pGammaRamp.Green[index]=60000;
				}
				break;

			case 4:
				for(index=0;index<230;index++)
				{
					pGammaRamp.Red[index]=62000; // some hindexgh valeu<ffoo
					pGammaRamp.Blue[index]=62000;
					pGammaRamp.Green[index]=62000;
				}
				for(index=230;index<256;index++)
				{
					pGammaRamp.Red[index]=65281;
					pGammaRamp.Blue[index]=65281;
					pGammaRamp.Green[index]=65281;
				}
				break;

			case 5: 		
				for(index=0;index<230;index++)
				{
					pGammaRamp.Red[index]=0; // some hindexgh valeu<ffoo
					pGammaRamp.Blue[index]=0;
					pGammaRamp.Green[index]=0;
				}
				break;

			case 6 :
				break;

			case 7 : 
				for(index=0;index<256;index++)
				{
					pGammaRamp.Green[index]=pGammaRamp.Blue[index]=pGammaRamp.Red[index]=index*256;			
				}
				break;

			case 8:
				for(index=0;index<49;index++)
				{
					pGammaRamp.Green[index]=pGammaRamp.Blue[index]=	pGammaRamp.Red[index]=0;			
				}
				for(index=49;index<256;index++)
				{
						pGammaRamp.Green[index]=pGammaRamp.Blue[index]=pGammaRamp.Red[index]=256*index;
				}
				break;

			case 9 :
				for(index=0;index<256;index++)
				{
					pGammaRamp.Green[index]=index*256;
					pGammaRamp.Blue[index]=index;
					pGammaRamp.Red[index]=index*256;			
				}
				break;

			case 10 :
				for(index=0;index<256;index++)
				{
					pGammaRamp.Green[index]=index*256;
					pGammaRamp.Blue[index]=index;
					pGammaRamp.Red[index]=index*512;			
				}
				break;
		
			case 11:
				break;
		}
	
		hr=SetGammaRamp(monitorID,&pGammaRamp,pExtraErrorCode,pErrorDescription);
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="pDispCfg"></param>
/// <param name="pPrimaryRR"></param>
/// <param name="pSecondaryRR"></param>
/// <param name="pErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetIndividualRefreshRate(REFRESHRATE *rr, REFRESHRATE refershrate[20], DWORD index,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	rr->usRefRate = refershrate[index].usRefRate;

	return hr;

}
STDMETHODIMP CDisplayUtil::GetCloneRefreshRate(/*[in]*/DISPLAY_CONFIG *pDispCfg,/*[out]*/ REFRESHRATE pPrimaryRR[20],/*[out]*/ REFRESHRATE pSecondaryRR[20],/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	DWORD dwExtraErrorCode=0;	
	DISPLAY_CONFIG DspCfg = {0};
	CComBSTR errorStr = L"";
	
	try
	{
		ZeroMemory(pPrimaryRR,20*sizeof(REFRESHRATE));
		ZeroMemory(pSecondaryRR,20*sizeof(REFRESHRATE));
			
		int nSizeRR=sizeof(REFRESHRATE)*20;
		int nSizeDC=sizeof(DISPLAY_CONFIG);			

		DspCfg.BPP = pDispCfg->BPP;
		DspCfg.uidMonitorPrimary = pDispCfg->uidMonitorPrimary;
		DspCfg.uidMonitorSecondary = pDispCfg->uidMonitorSecondary;
		DspCfg.XResolution = pDispCfg->XResolution;
		DspCfg.YResolution = pDispCfg->YResolution;

		

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetCloneRefreshRates(nSizeDC,(BYTE*)&DspCfg,nSizeRR,(BYTE*)pPrimaryRR,(BYTE*)pSecondaryRR,(DWORD*)pExtraErrorCode);
 		

		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		  return S_OK; 
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pDispCfg"></param>
/// <param name="pPrimaryRR"></param>
/// <param name="pSecondaryRR"></param>
/// <param name="pErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetCloneView(/*[in]*/DISPLAY_CONFIG *pDispCfg, /*[in]*/REFRESHRATE *pPrimaryRR,/*[in]*/ REFRESHRATE *pSecondaryRR,/*[out]*/ IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		int nSizeRR=sizeof(REFRESHRATE);
		int nSizeDC=sizeof(DISPLAY_CONFIG);
		
		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		hr=ptrCUIExternal->SetCloneView(nSizeDC, (BYTE *)pDispCfg,nSizeRR, (BYTE *)pPrimaryRR,(BYTE *)pSecondaryRR,(DWORD*)pExtraErrorCode);


		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS) 
			 return S_OK;
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetDVMTData(/*[out]*/IGFX_DVMT_1_0 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_DVMT_GUID_1_0;	
	CComBSTR errorStr = L"";
		
	try
	{
		int size=sizeof(IGFX_DVMT_1_0);
		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{			 
			return S_OK;	
		}
		
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetEDIDData(/*[out]*/IGFX_EDID_1_0 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_EDID_GUID_1_0; 
	CComBSTR errorStr = L"";
		
	try
	{
		int size=sizeof(IGFX_EDID_1_0);
 
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);
			
		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{			
			return S_OK;	
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::IsOverlayOn(/*[out]*/IGFX_OVERLAY_1_0 *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	// sending data from Ruby could be    aproblem as A Byte *  g\f rom RUBY 
	GUID structGUID=IGFX_OVERLAY_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{

		int size=sizeof(IGFX_OVERLAY_1_0);
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{		
			return S_OK;
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetOverScanData(/*[out]*/IGFX_SCALING_1_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_SCALING_GUID_1_0;		
	CComBSTR errorStr = L"";
		
	try
	{
		int size= sizeof(IGFX_SCALING_1_0);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		if(ptrCUIExternal == NULL)		{
			
			return hr;
		}

		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pData,(DWORD*)pExtraErrorCode);


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
/// 
/// </summary>
/// <param name="pData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetScaling(/*[out]*/IGFX_SCALING_2_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_GET_SET_SCALING2_GUID;		
	CComBSTR errorStr = L"";
		
	try
	{
		int size= sizeof(IGFX_SCALING_2_0);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		pData->versionHeader.dwVersion=1;
		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pData,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{			
			return S_OK;	
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


/// <summary>
/// 
/// </summary>
/// <param name="pData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetOverScanData(/*[in]*/IGFX_SCALING_1_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_SCALING_GUID_1_0;	
	CComBSTR errorStr = L"";
	
	try
	{
		int size= sizeof(IGFX_SCALING_1_0);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));							
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)pData,(DWORD*)pExtraErrorCode);

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
/// To set the desired scaling option
/// </summary>
/// <param name="pData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetScaling(/*[in]*/IGFX_SCALING_2_0 *pData,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_GET_SET_SCALING2_GUID;	
	CComBSTR errorStr = L"";
	try
	{
		int size= sizeof(IGFX_SCALING_2_0);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));							
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		pData->versionHeader.dwVersion=1;
		hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)pData,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{
			return S_OK;	
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}



/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::IsDownScalingSupported(/*[in]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;		
	CComBSTR errorStr = L"";
		 
	try
	{
		int nSize=sizeof(IGFX_DOWNSCALING_DATA);	

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));									
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

	    hr=ptrCUIExternal->IsDownScalingSupported(nSize,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{		 
			return S_OK;	
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}
	return hr;
}

/// <summary>
/// PURPOSE: To check if the DownScaling feature has  been enabled
/// </summary>
/// <param name="pbIsEnabled"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns>/// Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::IsDownScalingEnabled(/*[out]*/int *pbIsEnabled,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr = ptrCUIExternal->IsDownScalingEnabled((long*)pbIsEnabled,(DWORD*)pExtraErrorCode);
		if(FAILED(hr)) 
		{
			*pExtraErrorCode = IGFX_FAILURE;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To enable the Downscaling feature
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns>/// Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::EnableDownScaling(/*[in, out]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		int nSize=sizeof(IGFX_DOWNSCALING_DATA);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		hr=ptrCUIExternal->EnableDownScaling(nSize,(BYTE *)pBuffer,(DWORD*)pExtraErrorCode);
		if(FAILED(hr)) 
		{
			return S_OK;
		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To disable the Downscaling feature
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns>/// Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::DisableDownScaling(/*[in, out]*/IGFX_DOWNSCALING_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)	
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		int nSize=sizeof(IGFX_DOWNSCALING_DATA);

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		hr=ptrCUIExternal->DisableDownScaling(nSize,(BYTE *)pBuffer,(DWORD*)pExtraErrorCode);

		if(FAILED(hr)) 
		{
					
			return S_OK;

		}

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the configuration 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetConfiguration(/*[in]*/IGFX_DISPLAY_CONFIG_1_1 *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_DISPLAY_CONFIG_GUID_1_1;
	CComBSTR errorStr = L"";
	
	try
	{	
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		pBuffer->nSize = sizeof(IGFX_DISPLAY_CONFIG_1_1);
		hr=ptrCUIExternal->SetConfiguration((&structGUID), pBuffer->nSize,(BYTE *)pBuffer,(DWORD*)pExtraErrorCode);

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
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::Overlay_Set(/*[in, out]*/IGFX_OVERLAY_COLOR_SETTINGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_OVERLAY_COLOR_GUID_1_0;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}

			
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_OVERLAY_COLOR_SETTINGS),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);
		if(FAILED(hr)) 
		{
			return S_OK;
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::Overlay_Get(/*[in, out]*/IGFX_OVERLAY_COLOR_SETTINGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_OVERLAY_COLOR_GUID_1_0;
	CComBSTR errorStr = L"";

	try
	{
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			if(ptrCUIExternal == NULL)
			{
				
				return hr;
			}
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_OVERLAY_COLOR_SETTINGS),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::CVT_Get(/*[in, out]*/IGFX_FEATURE_SUPPORT_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_FEATURE_SUPPORT;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_FEATURE_SUPPORT_ARGS),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}
	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SDVO_Set(/*[in, out]*/IGFX_VENDOR_OPCODE_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SDVO_VENDOR_OPCODE_EXECUTION;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_VENDOR_OPCODE_ARGS),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSupportedConfiguration(/*[in, out]*/IGFX_TEST_CONFIG *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SUPPORTED_CONFIGURATIONS;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_TEST_CONFIG),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}



/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSupportedConfigurationEx(/*[in, out]*/IGFX_TEST_CONFIG_EX *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SUPPORTED_CONFIGURATIONS_EX ;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_TEST_CONFIG_EX),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}



/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetGraphicsModes(/*[in, out]*/IGFX_VIDEO_MODE_LIST *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	
	IGFX_VIDEO_MODE_LIST *modelist_data = new IGFX_VIDEO_MODE_LIST;
	GUID structGUID=IGFX_SUPPORTED_GRAPHICS_MODES;
	CComBSTR errorStr = L"";
	IGFX_TEST_CONFIG *buffer = new IGFX_TEST_CONFIG;
	GetSupportedConfiguration(buffer,pExtraErrorCode,&errorStr); 

    try
	{
		
		//	pBuffer = new IGFX_VIDEO_MODE_LIST;
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
			
		for(DWORD i=0; i < buffer->dwNumTotalCfg; i++)
		{
		modelist_data->dwOperatingMode =  buffer->ConfigList[i].dwOperatingMode;
		modelist_data->dwPriDevUID =  buffer->ConfigList[i].dwPriDevUID;
		modelist_data->dwSecDevUID =  buffer->ConfigList[i].dwSecDevUID;
		modelist_data->bIsPrimary = 1;     // 1 - graphics mode will be according to primary device
                                       // 0 - graphics mode will be according to secondry device                         


		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST),(BYTE*)modelist_data,(DWORD*)pExtraErrorCode);
		

		pBuffer->vmlNumModes = modelist_data->vmlNumModes;
		pBuffer->bIsPrimary = modelist_data->bIsPrimary;
		pBuffer->dwOperatingMode = modelist_data->dwOperatingMode;
		pBuffer->dwPriDevUID = modelist_data->dwPriDevUID ;
		pBuffer->dwReserved1 = modelist_data->dwReserved1;
		pBuffer->dwReserved2 = modelist_data->dwReserved2;
		pBuffer->dwSecDevUID = modelist_data->dwSecDevUID;
 		
	   for(WORD j=0; j<modelist_data->vmlNumModes; j++)
		   
       {
         pBuffer->vmlModes[j].dwHzRes = modelist_data->vmlModes[j].dwHzRes;
		 pBuffer->vmlModes[j].dwVtRes = modelist_data->vmlModes[j].dwVtRes;
         pBuffer->vmlModes[j].dwRR = modelist_data->vmlModes[j].dwRR;
		 pBuffer->vmlModes[j].dwBPP = modelist_data->vmlModes[j].dwBPP;

	   }


		if(FAILED(hr)) 
		{
			return ErrorHandler(L"GetGraphicsModes::GetDeviceData",hr,pErrorDescription);
		}
	}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSupportedGraphicsModes(/*[in, out]*/IGFX_VIDEO_MODE_LIST *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SUPPORTED_GRAPHICS_MODES;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Queries for the number of video modes available. the video modes are cached in a static variable. 
/// After this call the client has to loop thru the GetIndividualVideoMode call to  get the individual video modes.
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::QueryforVideoModeList(/*[in,out]*/ IGFX_VIDEO_MODE_LIST_EX *pVideoModeList,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_VIDEO_MODE_LIST_GUID;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
			pVideoModeList->dwFlags=1;
			pVideoModeList->versionHeader.dwVersion = 1;
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST_EX),(BYTE*)pVideoModeList,(DWORD*)pExtraErrorCode);
			int noModes=pVideoModeList->vmlNumModes;
			int size=sizeof(IGFX_VIDEO_MODE_LIST_EX) + (sizeof(IGFX_DISPLAY_RESOLUTION_EX)*(noModes-1));
			IGFX_VIDEO_MODE_LIST_EX *pVideoModeList1=(IGFX_VIDEO_MODE_LIST_EX*) malloc (size);
			pVideoModeList1->dwFlags=0;
			pVideoModeList1->versionHeader=pVideoModeList->versionHeader;
			pVideoModeList1->dwOpMode=pVideoModeList->dwOpMode;
			pVideoModeList1->uiNDisplays=pVideoModeList->uiNDisplays;
			for(int index=0;index<6;index++)
			{
			pVideoModeList1->DispCfg[index]=pVideoModeList->DispCfg[index];
			}
			pVideoModeList1->dwDeviceID=pVideoModeList->dwDeviceID;
			pVideoModeList1->vmlNumModes=pVideoModeList->vmlNumModes;
			hr=ptrCUIExternal->GetDeviceData(&structGUID, size,(BYTE*)pVideoModeList1,(DWORD*)pExtraErrorCode);
			pVideoModes=(IGFX_DISPLAY_RESOLUTION_EX*)malloc(sizeof(IGFX_DISPLAY_RESOLUTION_EX)*noModes);
			for(int index=0;index<noModes;index++)
			{
				pVideoModes[index]=pVideoModeList1->vmlModes[index];
			}
			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

STDMETHODIMP CDisplayUtil::GetVideoModeListEx(/*[in,out]*/ IGFX_VIDEO_MODE_LIST_EX *pVideoModeListEx,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_VIDEO_MODE_LIST_GUID;
	CComBSTR errorStr = L"";

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
			pVideoModeListEx->dwFlags=1;			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST_EX),(BYTE*)pVideoModeListEx,(DWORD*)pExtraErrorCode);
			int noModes=pVideoModeListEx->vmlNumModes;
			int size=sizeof(IGFX_VIDEO_MODE_LIST_EX) + (sizeof(IGFX_DISPLAY_RESOLUTION_EX)*(noModes-1));
			IGFX_VIDEO_MODE_LIST_EX *pVideoModeListEx1=(IGFX_VIDEO_MODE_LIST_EX*) malloc (size);
			pVideoModeListEx1->dwFlags=0;
			pVideoModeListEx1->versionHeader=pVideoModeListEx->versionHeader;
			pVideoModeListEx1->dwOpMode=pVideoModeListEx->dwOpMode;
			pVideoModeListEx1->uiNDisplays=pVideoModeListEx->uiNDisplays;
			for(int index=0;index<6;index++)
			{
			pVideoModeListEx1->DispCfg[index]=pVideoModeListEx->DispCfg[index];
			}
			pVideoModeListEx1->dwDeviceID=pVideoModeListEx->dwDeviceID;
			pVideoModeListEx1->vmlNumModes=pVideoModeListEx->vmlNumModes;
			hr=ptrCUIExternal->GetDeviceData(&structGUID, size,(BYTE*)pVideoModeListEx1,(DWORD*)pExtraErrorCode);
			pVideoModes=(IGFX_DISPLAY_RESOLUTION_EX*)malloc(sizeof(IGFX_DISPLAY_RESOLUTION_EX)*noModes);
			for(int index=0;index<noModes;index++)
			{
				pVideoModes[index]=pVideoModeListEx1->vmlModes[index];
			}
			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}






/*STDMETHODIMP CDisplayUtil::QueryforDispCfg(IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pVideoModeList,IGFX_ERROR_CODES *pExtraErrorCode, BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_N_VIEW_CONFIG_GUID;
	CComBSTR errorStr = L"";

	try
	{
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_CONFIG_DATA_N_VIEW),(BYTE*)pVideoModeList,(DWORD*)pExtraErrorCode);
			pVideoModeList->dwFlags=0;
			int noDisp=pVideoModeList->uiNDisplays;
			int size=sizeof(IGFX_SYSTEM_CONFIG_DATA_N_VIEW) + (sizeof(IGFX_DISPLAY_CONFIG_DATA_EX)*(noDisp-1));
			IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pVideoModeList1=(IGFX_SYSTEM_CONFIG_DATA_N_VIEW*) malloc (size);
			pVideoModeList1->dwFlags=0;
			pVideoModeList1->dwOpMode=pVideoModeList->dwOpMode;
			pVideoModeList1->uiNDisplays=pVideoModeList->uiNDisplays;
			pVideoModeList1->uiSize=pVideoModeList->uiSize;
			hr=ptrCUIExternal->GetDeviceData(&structGUID, size,
				(BYTE*)pVideoModeList1,(DWORD*)pExtraErrorCode);
			pDispCfg=(IGFX_DISPLAY_CONFIG_DATA_EX *)malloc(sizeof(IGFX_DISPLAY_CONFIG_DATA_EX)*noDisp);
			for(int index=0;index<noDisp;index++)
			{
				pDispCfg[index]=pVideoModeList1->DispCfg[index];
			}
			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
	
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}*/

/// <summary>
/// This call should be made after query for the Video Modes is made to get the individual video modes.
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetIndividualVideoMode(/*[in,out]*/ IGFX_DISPLAY_RESOLUTION_EX *pVideoMode, DWORD index,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/ BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		pVideoMode[0] = pVideoModes[index];
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;

}


/*STDMETHODIMP CDisplayUtil::GetIndividualCfg( IGFX_DISPLAY_CONFIG_DATA_EX *pVideoMode, DWORD index,IGFX_ERROR_CODES *pExtraErrorCode, BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		pVideoMode[0] = pDispCfg[index];
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
	
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;

}*/

/*
HRESULT CUISDKDLL_API InitCUISDK()
{
	HRESULT hr= S_OK;
	HRESULT hr1= S_OK;

	hr = CoInitialize(NULL);

	if(SUCCEEDED(hr))
	{
		hr = ::CoCreateInstance(CLSID_CUIExternal,NULL,	CLSCTX_SERVER,IID_ICUIExternal8,(void **)&pCUIExternal);//get interface pointer
		if(SUCCEEDED(hr))
		{
			printf(" \n COCreate Instance Succeeded for  8 \n\n");
            hr1 = pCUIExternal->QueryInterface(IID_ICUIDownScale,(void ** )&pCUIDownScale);
            if (SUCCEEDED(hr1))
			{
			  printf (" QUERY INTERFACE SUCCESSFUL FOR IID_ICUIDownScale\n\n ");
			}
			else
			{
				// printf("\n QI for IID_ICUIDownscale Failed ");
			}
			return hr ;
		}
		else // COcreate faild for ICUIEXternalinterface8
		{
			printf(" COCREATE FAILEDS FOR 8 so no win 7 ");
			hr = ::CoCreateInstance(CLSID_CUIExternal,NULL,	CLSCTX_SERVER,IID_ICUIExternal7,(void **)&pCUIExternal);

			if(SUCCEEDED(hr))
			{
				printf(" \n COCreate Instance Succeeded for  7\n\n");
				maxIntefaceSupported=7;
				// For dwonscaling//
		     hr1=pCUIExternal->QueryInterface(IID_ICUIDownScale,(void ** )&pCUIDownScale);
  			 if (SUCCEEDED(hr1))
			 {
				printf (" QUERY INTERFACE SUCCESSFUL ");
			 }

			return hr ;

		}
		else
		{
			printf("failed second time for  7..");
							
			// try for 6 
			hr= ::CoCreateInstance(CLSID_CUIExternal,NULL,CLSCTX_SERVER,IID_ICUIExternal6,(void **)&pCUIExternal);

			if(SUCCEEDED(hr))
			{
				printf(" \n COCreate Instance Succeeded for  6\n\n");
				maxIntefaceSupported=6;
			
			     hr1=pCUIExternal->QueryInterface(IID_ICUIDownScale,(void ** )&pCUIDownScale);
							if (SUCCEEDED(hr1))
							{

							printf (" QUERY INTERFACE SUCCESSFUL ");
			
							 }

						//

						return hr ;

						}

					
					}


			// continue trying till 5 
			}



	
	}//  If (Coinitilization)
	
	return hr;
}


HRESULT CUISDKDLL_API ExitCUISDK()
{
	HRESULT hr= S_OK;
   if(pCUIExternal != NULL)
   {
      hr = pCUIExternal->Release();
   }

	if(pCUIDownScale=NULL)
	{
	 hr=pCUIDownScale->Release();
	}

// mjm - missed initilasing to Null ??


   ::CoUninitialize();

  return hr;
}
*/
/// <summary>
/// Purpose: To get the VBIOS version
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetVBIOSVersion(/*[in, out]*/BSTR *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	CComBSTR errorStr = L"";
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_VBIOS_VERSION_GUID;
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		DWORD vbiosVer = 0;
		DWORD extraErrorCode=0;
		hr = ptrCUIExternal->GetDeviceData(&structGUID,sizeof(DWORD),(BYTE *)&vbiosVer,(DWORD*)pExtraErrorCode);
		if (SUCCEEDED(hr) && *pExtraErrorCode == IGFX_SUCCESS)
		{
			char chVBIOSVersion[5]={0};
			sprintf(chVBIOSVersion,"%ld",vbiosVer);
			CComBSTR VBIOSVersion(chVBIOSVersion);
			//send the result back to clients
			*pBuffer = VBIOSVersion.Copy();
		}
		else
		{
			*pErrorDescription = L"Error while getting VBIOS Version";
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription = errorStr.Copy();
		
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
/// Purpose: To get the recently set Gamma
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetGammaBrightnessContrast(/*[in, out]*/IGFX_DESKTOP_GAMMA_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	CComBSTR errorStr = L"";
	HRESULT hr = S_OK;
	GUID structGUID=IGFX_DESKTOP_GAMMA;

	int size= sizeof(IGFX_DESKTOP_GAMMA_ARGS);

	try
	{
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

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


/// <summary>
/// 
/// </summary>
/// <param name="gamma"></param>
/// <param name="bright"></param>
/// <param name="con"></param>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetGammaBrightnessContrast(/*[in, out]*/IGFX_DESKTOP_GAMMA_ARGS *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID=IGFX_DESKTOP_GAMMA;

	int size= sizeof(IGFX_DESKTOP_GAMMA_ARGS);

	try
	{
		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// 
/// </summary>
/// <param name="sysConfigData"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="opmode"></param>
/// <param name="PriRotAngle"></param>
/// <param name="SecRotAngle"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetSystemConfigurationAll(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *sysConfigData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[in]*/DWORD opmode,/*[in]*/DWORD PriRotAngle,/*[in]*/DWORD SecRotAngle,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{	
  
        IGFX_VIDEO_MODE_LIST *modelist_data = new IGFX_VIDEO_MODE_LIST;
        IGFX_VIDEO_MODE_LIST *modelist_dataS = new IGFX_VIDEO_MODE_LIST;
        IGFX_TEST_CONFIG *buffer = new IGFX_TEST_CONFIG;
        
        GetSupportedConfiguration(buffer,pExtraErrorCode,pErrorDescription);

        for(DWORD i=0; i < buffer->dwNumTotalCfg; i++)
        {               
            if( (opmode == 0) || (buffer->ConfigList[i].dwOperatingMode == opmode)) 	
            {
                modelist_data->dwOperatingMode =  buffer->ConfigList[i].dwOperatingMode;
                modelist_data->dwPriDevUID =  buffer->ConfigList[i].dwPriDevUID;
                modelist_data->dwSecDevUID =  buffer->ConfigList[i].dwSecDevUID;
                modelist_data->bIsPrimary = 1;     // 1 - graphics mode will be according to primary device
                // 0 - graphics mode will be according to secondry device                         
         
                GUID structGUID=IGFX_SUPPORTED_GRAPHICS_MODES; 


                if(NULL != ptrCUIExternal)
                {     
                    hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST),(BYTE*)modelist_data,(DWORD *)pExtraErrorCode);
                    ::Sleep(5);

                    if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                    {
                        for(WORD j=0; j<modelist_data->vmlNumModes; j++)
                        {
                            sysConfigData->dwOpMode    = buffer->ConfigList[i].dwOperatingMode;
                            sysConfigData->PriDispCfg.dwDisplayUID          = buffer->ConfigList[i].dwPriDevUID;
                            sysConfigData->SecDispCfg.dwDisplayUID          = buffer->ConfigList[i].dwSecDevUID;
                            sysConfigData->PriDispCfg.Resolution.dwHzRes   = modelist_data->vmlModes[j].dwHzRes;
                            sysConfigData->PriDispCfg.Resolution.dwVtRes   = modelist_data->vmlModes[j].dwVtRes; // for 180 or 0 degree
                            sysConfigData->PriDispCfg.Resolution.dwRR      = modelist_data->vmlModes[j].dwRR;
                            sysConfigData->PriDispCfg.Resolution.dwBPP     = modelist_data->vmlModes[j].dwBPP;
                            sysConfigData->PriDispCfg.dwOrientation        = PriRotAngle|IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION ;

                            if((PriRotAngle ==1 || PriRotAngle ==3) && (sysConfigData->PriDispCfg.Resolution.dwHzRes > sysConfigData->PriDispCfg.Resolution.dwVtRes))
                            {
                                DWORD x;
                                x =sysConfigData->PriDispCfg.Resolution.dwHzRes;
                                sysConfigData->PriDispCfg.Resolution.dwHzRes = sysConfigData->PriDispCfg.Resolution.dwVtRes;
                                sysConfigData->PriDispCfg.Resolution.dwVtRes = x;
                            }

                            if(buffer->ConfigList[i].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE||buffer->ConfigList[i].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDTWIN )
                            {
                                if(buffer->ConfigList[i].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDTWIN)
                                {
                                sysConfigData->SecDispCfg.Resolution.dwHzRes   = sysConfigData->PriDispCfg.Resolution.dwHzRes;
                                sysConfigData->SecDispCfg.Resolution.dwVtRes    = sysConfigData->PriDispCfg.Resolution.dwVtRes;
                                sysConfigData->SecDispCfg.Resolution.dwRR     = sysConfigData->PriDispCfg.Resolution.dwRR;
                                sysConfigData->SecDispCfg.Resolution.dwBPP     = sysConfigData->PriDispCfg.Resolution.dwBPP;
                                sysConfigData->SecDispCfg.dwOrientation     = sysConfigData->PriDispCfg.dwOrientation;
                                }


                                GUID structGUID=IGFX_GET_SET_CONFIGURATION_GUID;


                                ::Sleep(150);

                                hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_CONFIG_DATA),(BYTE*)sysConfigData,(DWORD *)pExtraErrorCode);

                                if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                                {
                                    //printf("succeeded in Setting ..** 2 ** .. \n");
                                }   
                                else
                                {
                                    //printf("Failed in setting** 2 ** \n");
                                    //printf (" \n\nError Code :: %u",*pExtraErrorCode);
                                    return hr;  //disbale //
                                }
                            }
                            else
                            {
                                modelist_dataS->dwOperatingMode =  buffer->ConfigList[i].dwOperatingMode;
                                modelist_dataS->dwPriDevUID =      buffer->ConfigList[i].dwPriDevUID;
                                modelist_dataS->dwSecDevUID =      buffer->ConfigList[i].dwSecDevUID;
                                modelist_dataS->bIsPrimary = 0;     // 1 - graphics mode will be according to primary device
                                // 0 - graphics mode will be according to secondry device   

                                GUID structGUID=IGFX_SUPPORTED_GRAPHICS_MODES;
                                hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_MODE_LIST),(BYTE*)modelist_dataS,(DWORD *)pExtraErrorCode);
                                ::Sleep(5);
                                
                                if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                                {
                                    for(WORD k=0; k<modelist_dataS->vmlNumModes; k++)
                                    {                                      
                                        if(buffer->ConfigList[i].dwOperatingMode == IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE)
                                        {
                                            sysConfigData->SecDispCfg.Resolution.dwHzRes   = sysConfigData->PriDispCfg.Resolution.dwHzRes;
                                            sysConfigData->SecDispCfg.Resolution.dwVtRes    = sysConfigData->PriDispCfg.Resolution.dwVtRes;
                                            sysConfigData->SecDispCfg.Resolution.dwBPP     = sysConfigData->PriDispCfg.Resolution.dwBPP;
                                        }
                                        else
                                        {
                                            sysConfigData->SecDispCfg.Resolution.dwHzRes   = modelist_dataS->vmlModes[k].dwHzRes;
                                            sysConfigData->SecDispCfg.Resolution.dwVtRes    = modelist_dataS->vmlModes[k].dwVtRes;
                                            sysConfigData->SecDispCfg.Resolution.dwBPP     = modelist_dataS->vmlModes[k].dwBPP;
                                        }
                                        
                                        k = modelist_dataS->vmlNumModes -1; //??
                                        sysConfigData->SecDispCfg.Resolution.dwRR      = modelist_dataS->vmlModes[k].dwRR;
                                        sysConfigData->SecDispCfg.dwOrientation        = SecRotAngle|IGFX_DISPLAY_CONFIG_FLAG_ORIENTATION ;
                                        
                                        if((SecRotAngle ==1 || SecRotAngle ==3) && (sysConfigData->SecDispCfg.Resolution.dwHzRes > sysConfigData->SecDispCfg.Resolution.dwVtRes))
                                        {
                                            DWORD x;
                                            x =sysConfigData->SecDispCfg.Resolution.dwHzRes;
                                            sysConfigData->SecDispCfg.Resolution.dwHzRes = sysConfigData->SecDispCfg.Resolution.dwVtRes;
                                            sysConfigData->SecDispCfg.Resolution.dwVtRes = x;
                                        }
                                        
                                        sysConfigData->SecDispCfg.Position.iLeft       = sysConfigData->PriDispCfg.Resolution.dwHzRes;//primary
                                        sysConfigData->SecDispCfg.Position.iTop       = sysConfigData->PriDispCfg.Resolution.dwVtRes;//primary
                                        sysConfigData->SecDispCfg.Position.iRight       = sysConfigData->SecDispCfg.Position.iLeft + modelist_dataS->vmlModes[k].dwHzRes;
                                        sysConfigData->SecDispCfg.Position.iBottom      = sysConfigData->SecDispCfg.Position.iTop  + modelist_dataS->vmlModes[k].dwVtRes;

                                        GUID structGUID=IGFX_GET_SET_CONFIGURATION_GUID;
                                        ::Sleep(200);

                                        hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_CONFIG_DATA),(BYTE*)sysConfigData,(DWORD *)pExtraErrorCode);
                                        if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                                        {
                                            //printf("succeeded in Setting .** 4 ** ... \n");
                                        }  
                                        else
                                        {
                                            //printf("Failed in setting ** 4 ** \n");
                                            //printf (" \n\nError Code :: %u",*pExtraErrorCode);
                                            return hr;  // disable
                                        }                                      
                                    }//For
                                }//If  of if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)                                  
                                else
                                {
                                    //printf("Failed in Getting ** 3 ** \n");
                                    //printf (" \n\nError Code :: %u",*pExtraErrorCode);
                                    return hr;
                                }//Else  of if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                            }// Else
                        } //For loop
                    } //if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                    else
                    {
                        printf("Failed in Getting ** 1 ** \n");
                        printf (" \n\nError Code :: %u",*pExtraErrorCode);
                        return hr;
                    }//else of if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
                } 
                else
                {
                    //printf(" \n\nInterface problem or the  DRIVER  Does not Support  this Inteface  Function.\n Max supported interfcae:%d",maxIntefaceSupported);
                    return hr;
                } // if(NULL != ptrCUIExternal && maxIntefaceSupported>7)
            }
        }//end of for
	}
	catch(_com_error& error)
	{
			errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the system configuration
/// </summary>
/// <param name="sysConfigData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetSystemConfiguration(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *sysConfigData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_CONFIGURATION_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_CONFIG_DATA),(BYTE*)sysConfigData,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{					
				return S_OK;
			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To get the system configuration
/// </summary>
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSystemConfiguration(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA *pBuffer, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_CONFIGURATION_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_SYSTEM_CONFIG_DATA),(BYTE*)pBuffer,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{					
				return S_OK;
			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="mediaScalarData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetMediaScalar(/*[in, out]*/IGFX_MEDIA_SCALAR *mediaScalarData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_GET_SET_MEDIASCALAR_GUID;

	try
	{		
		{ 
			int size = sizeof(IGFX_MEDIA_SCALAR);
			
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)mediaScalarData,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Gets MediaScalar 
/// </summary>
/// <param name="mediaScalarData"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetMediaScalar(/*[in, out]*/IGFX_MEDIA_SCALAR *mediaScalarData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_GET_SET_MEDIASCALAR_GUID;

	try
	{
		int size= sizeof(IGFX_MEDIA_SCALAR);
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)mediaScalarData,(DWORD*)pExtraErrorCode);
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
/// Purpose: to Initialize the custom mode array
/// </summary>
/// <param name="monid"></param>
/// <param name="i"></param>
/// <param name="HzR"></param>
/// <param name="VtR"></param>
/// <param name="RR"></param>
/// <param name="BPP"></param>
/// <param name="Imode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::InitilizeRemoveCustomModeArray(/*[in]*/DWORD monid,/*[in]*/DWORD i,/*[in]*/DWORD HzR,/*[in]*/DWORD VtR,/*[in]*/DWORD RR,/*[in]*/DWORD BPP,/*[in]*/DWORD Imode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	IGFX_CUSTOM_MODELIST *rcm = new IGFX_CUSTOM_MODELIST;

	try
	{
		   	 
	  rcm->dwDisplayUID		 = monid;
	  rcm->dwTotalModes		 = i+1;  

	  rcm->ModeList[i].dwHzRes			 = HzR;
	  rcm->ModeList[i].dwVtRes			 = VtR;
	  rcm->ModeList[i].dwRR				 = RR ;
	  rcm->ModeList[i].dwBPP			 = BPP;
	  rcm->ModeList[i].bInterlacedMode   = Imode ;

return 0;

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
/// Purpose: To remove the custom mode array
/// </summary>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::RemoveCustomMode(/*[in]*/IGFX_CUSTOM_MODELIST *pCustomModeList, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID=IGFX_REMOVE_CUSTOM_MODELIST_GUID ;
	
	IGFX_CUSTOM_MODELIST *rcm = new IGFX_CUSTOM_MODELIST;
	rcm->dwDisplayUID = pCustomModeList->dwDisplayUID;
	rcm->dwFlags = pCustomModeList->dwFlags;
	rcm->dwTotalModes = pCustomModeList->dwTotalModes;
	
	for(int index =0;index < rcm->dwTotalModes;index++)
	{
		rcm->ModeList[index].bInterlacedMode = pCustomModeList->ModeList[index].bInterlacedMode;
		rcm->ModeList[index].dwBPP = pCustomModeList->ModeList[index].dwBPP;
		rcm->ModeList[index].dwHzRes = pCustomModeList->ModeList[index].dwHzRes;
		rcm->ModeList[index].dwRR = pCustomModeList->ModeList[index].dwRR;
		rcm->ModeList[index].dwVtRes = pCustomModeList->ModeList[index].dwVtRes;
	}


	 printf("\n\nRemoved these modes successfully"); 
	 printf("\n\nMonID					   = %u\n",rcm->dwDisplayUID);
     printf(" Total modes be removed.. = %u\n\n", rcm->dwTotalModes);

	for(DWORD i=0; i< rcm->dwTotalModes ;i++)
	{
   printf(" %dHorizontal Resolution  = %u\n",i,rcm->ModeList[i].dwHzRes);
   printf(" %dVertical Resolution    = %u\n",i,rcm->ModeList[i].dwVtRes);
   printf(" %dRefresh Rate           = %u\n",i,rcm->ModeList[i].dwRR);
   printf(" %dColor Depth		 = %u\n",i,rcm->ModeList[i].dwBPP);
   printf(" %dInterlace Mode         = %u\n\n",i,rcm->ModeList[i].bInterlacedMode);
	}
   

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_CUSTOM_MODELIST),(BYTE*)rcm,(DWORD*)pExtraErrorCode);
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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To add the advanced custom mode
/// </summary>
/// <param name="advancedCustomMode"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::AddAdvancedCustomMode(/*[in, out]*/IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA *advancedCustomMode, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_ADD_ADVANCED_CUSTOM_MODE_GUID;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_ADD_ADVANCED_CUSTOM_MODE_DATA),(BYTE*)advancedCustomMode,(DWORD*)pExtraErrorCode);
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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To add the basic custom mode
/// </summary>
/// <param name="basicCustomMode"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::AddBasicCustomMode(/*[in, out]*/IGFX_ADD_BASIC_CUSTOM_MODE_DATA *basicCustomMode, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_ADD_BASIC_CUSTOM_MODE_GUID;

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_ADD_BASIC_CUSTOM_MODE_DATA),(BYTE*)basicCustomMode,(DWORD*)pExtraErrorCode);
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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To get the custom mode timing
/// </summary>
/// <param name="customModeTiming"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetCustomModeTiming(/*[in, out]*/IGFX_CUSTOM_MODE_TIMING_DATA *customModeTiming, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_GET_CUSTOM_MODE_TIMING_GUID;

	try
	{
		
		
	
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_CUSTOM_MODE_TIMING_DATA),(BYTE*)customModeTiming,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


/// <summary>
/// Purpose: To get the Custom mode list
/// </summary>
/// <param name="customModeList"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetCustomModeList(/*[in, out]*/IGFX_CUSTOM_MODELIST *customModeList, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_CUSTOM_MODELIST_GUID;
	CComBSTR errorStr = L"";

	try
	{		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_CUSTOM_MODELIST),(BYTE*)customModeList,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="mediaScaling"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetMediaScaling(/*[in, out]*/IGFX_MEDIA_SCALING_DATA *mediaScaling, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_GET_SET_MEDIA_SCALING_GUID;

	try
	{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_MEDIA_SCALING_DATA),(BYTE*)mediaScaling,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="mediaScaling"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetMediaScaling(/*[in, out]*/IGFX_MEDIA_SCALING_DATA *mediaScaling, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_MEDIA_SCALING_GUID;
	CComBSTR errorStr = L"";

	try
	{
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				

			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MEDIA_SCALING_DATA),(BYTE*)mediaScaling,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


STDMETHODIMP CDisplayUtil::GetMediaScalingEx2(/*[in, out]*/IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_MEDIA_SCALING_EX2_GUID;
	CComBSTR errorStr = L"";

	try
	{
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				

			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MEDIA_SCALING_DATA_EX2),(BYTE*)mediaScalingEx2,(DWORD*)pExtraErrorCode);
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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="mediaColor"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetMediaScalingEx2/*[in, out]*/(IGFX_MEDIA_SCALING_DATA_EX2 *mediaScalingEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_MEDIA_SCALING_EX2_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_MEDIA_SCALING_DATA_EX2),(BYTE*)mediaScalingEx2,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}
/// <summary>
/// 
/// </summary>
/// <param name="mediaColor"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetMediaColor/*[in, out]*/(IGFX_MEDIA_COLOR_DATA *mediaColor, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_MEDIA_COLOR_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_MEDIA_COLOR_DATA),(BYTE*)mediaColor,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="mediaColor"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetMediaColor(/*[in, out]*/IGFX_MEDIA_COLOR_DATA *mediaColor, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_MEDIA_COLOR_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				

			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MEDIA_COLOR_DATA),(BYTE*)mediaColor,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the video quality
/// </summary>
/// <param name="videoQuality"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetVideoQuality(/*[in, out]*/IGFX_VIDEO_QUALITY_DATA *videoQuality, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_VIDEO_QUALITY_GUID;
	CComBSTR errorStr = L"";

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				

			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_VIDEO_QUALITY_DATA),(BYTE*)videoQuality,(DWORD*)pExtraErrorCode);

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
/// Purpose: To get the video quality
/// </summary>
/// <param name="videoQuality"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetVideoQuality(/*[in, out]*/IGFX_VIDEO_QUALITY_DATA *videoQuality, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID=IGFX_GET_SET_VIDEO_QUALITY_GUID;
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_QUALITY_DATA),(BYTE*)videoQuality,(DWORD*)pExtraErrorCode);
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
/// Purpose: To get the Avi information frame
/// </summary>
/// <param name="aviInfoFrame"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetAviInfoFrame(/*[in, out]*/IGFX_AVI_INFOFRAME *aviInfoFrame, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AVI_INFOFRAME_GUID;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_AVI_INFOFRAME),(BYTE*)aviInfoFrame,(DWORD*)pExtraErrorCode);
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
/// Purpose: To set the Avi information frame 
/// </summary>
/// <param name="aviInfoFrame"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetAviInfoFrame(/*[in, out]*/IGFX_AVI_INFOFRAME *aviInfoFrame, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AVI_INFOFRAME_GUID;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AVI_INFOFRAME),(BYTE*)aviInfoFrame,(DWORD*)pExtraErrorCode);
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
/// Purpose: To get the Avi information frame
/// </summary>
/// <param name="aviInfoFrame"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetAviInfoFrameEx(/*[in, out]*/IGFX_AVI_INFOFRAME_EX *aviInfoFrameEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AVI_INFOFRAME_EX_GUID;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_AVI_INFOFRAME_EX),(BYTE*)aviInfoFrameEx,(DWORD*)pExtraErrorCode);
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
/// Purpose: To set the Avi information frame 
/// </summary>
/// <param name="aviInfoFrame"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetAviInfoFrameEx(/*[in, out]*/IGFX_AVI_INFOFRAME_EX *aviInfoFrameEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AVI_INFOFRAME_EX_GUID;
	CComBSTR errorStr = L"";

	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));			
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AVI_INFOFRAME_EX),(BYTE*)aviInfoFrameEx,(DWORD*)pExtraErrorCode);
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

STDMETHODIMP CDisplayUtil::GetHueSaturation(/*[in,out]*/ IGFX_HUESAT_INFO *pHueSat, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_HUESAT_INFO_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_HUESAT_INFO),(BYTE*)pHueSat,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CDisplayUtil::SetHueSaturation(/*[in,out]*/ IGFX_HUESAT_INFO *pHueSat, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_HUESAT_INFO_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_HUESAT_INFO),(BYTE*)pHueSat,(DWORD*)pExtraErrorCode);

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
STDMETHODIMP CDisplayUtil::GetVideoQualityExtended(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_VIDEO_QUALITY_EX_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_VIDEO_QUALITY_DATA_EX),(BYTE*)pVideoQualityEx,(DWORD*)pExtraErrorCode);
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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

STDMETHODIMP CDisplayUtil::SetVideoQualityExtended(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX *pVideoQualityEx, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_VIDEO_QUALITY_EX_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_VIDEO_QUALITY_DATA_EX),(BYTE*)pVideoQualityEx,(DWORD*)pExtraErrorCode);

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
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}


STDMETHODIMP CDisplayUtil::GetVideoFeatureSupportList(/*[in,out]*/IGFX_FEATURE_SUPPORT_ARGS *pVideoSupportList, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_FEATURE_SUPPORT;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_FEATURE_SUPPORT_ARGS),(BYTE*)pVideoSupportList,(DWORD*)pExtraErrorCode);

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
/// Purpose: To Get the Video Quality Data
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetVideoQualityExtended2(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_VIDEO_QUALITY_EX2_GUID;
	DWORD size = sizeof(IGFX_VIDEO_QUALITY_DATA_EX2);	
	if(pVideoQualityEx2->header.dwVersion == 3)
		size = size - (sizeof(float)*5);
	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pVideoQualityEx2,(DWORD*)pExtraErrorCode);

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
/// Purpose: To Set the Video Quality Data
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetVideoQualityExtended2(/*[in,out]*/IGFX_VIDEO_QUALITY_DATA_EX2 *pVideoQualityEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_VIDEO_QUALITY_EX2_GUID;
	DWORD size = sizeof(IGFX_VIDEO_QUALITY_DATA_EX2);	
	if(pVideoQualityEx2->header.dwVersion == 3)
		size = size - (sizeof(float)*5);

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)pVideoQualityEx2,(DWORD*)pExtraErrorCode);

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
/// Purpose: To Get the Media Color Data
/// </summary>
/// <param name="pMediaColorEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetMediaColorExtended2(/*[in,out]*/IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	
	
	GUID structGUID = IGFX_GET_SET_MEDIA_COLOR_EX2_GUID;

	DWORD size = sizeof(IGFX_MEDIA_COLOR_DATA_EX2);	
	if(pMediaColorEx2->header.dwVersion == 1)
		size = size - (sizeof(DWORD)*2);
		
	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,size,(BYTE*)pMediaColorEx2,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To Set the Media Color Data
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetMediaColorExtended2(/*[in,out]*/IGFX_MEDIA_COLOR_DATA_EX2 *pMediaColorEx2, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_MEDIA_COLOR_EX2_GUID;


	DWORD size = sizeof(IGFX_MEDIA_COLOR_DATA_EX2);	
	if(pMediaColorEx2->header.dwVersion == 1)
		size = size - (sizeof(DWORD)*2);
	
	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,size,(BYTE*)pMediaColorEx2,(DWORD*)pExtraErrorCode);

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

// <summary>
/// Purpose: To Get the Media Gamut
/// </summary>
/// <param name="pMediaColorEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetVideoGamutMapping(/*[in,out]*/IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_MEDIA_GAMUT_MAPPING;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MEDIA_GAMUT_MAPPING),(BYTE*)pMediaGamutMapping,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To Set the Media Gamut
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetVideoGamutMapping(/*[in,out]*/IGFX_MEDIA_GAMUT_MAPPING *pMediaGamutMapping, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_MEDIA_GAMUT_MAPPING;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_MEDIA_GAMUT_MAPPING),(BYTE*)pMediaGamutMapping,(DWORD*)pExtraErrorCode);

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
/// <summary>
/// Purpose: To get the system configuration data
/// </summary>
/// <param name="dataNView"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetSystemConfigDataNView(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEW *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_N_VIEW_CONFIG_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,dataNView->uiSize,(BYTE*)dataNView,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To set the system configuration data 
/// Wrapper for SetSystemConfigDataNView-- for use in c#
/// </summary>
/// <param name="dataNView"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetSystemConfigDataNViews(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	GUID structGUID = IGFX_GET_SET_N_VIEW_CONFIG_GUID;
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		/*IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pDataNView=(IGFX_SYSTEM_CONFIG_DATA_N_VIEW *)dataNView;
		hr=SetSystemConfigDataNView(pDataNView,pExtraErrorCode,pErrorDescription);*/
		hr=ptrCUIExternal->SetDeviceData(&structGUID,dataNView->uiSize,(BYTE*)dataNView,(DWORD*)pExtraErrorCode);
		if(FAILED(hr)) 
		{
			return S_OK;
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
/// Purpose: To get the system configuration data 
/// </summary>
/// <param name="dataNView"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSystemConfigDataNView(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEW *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID = IGFX_GET_SET_N_VIEW_CONFIG_GUID ;
	CComBSTR errorStr = L"";
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		hr=ptrCUIExternal->GetDeviceData(&structGUID,dataNView->uiSize,(BYTE*)dataNView,(DWORD*)pExtraErrorCode);
		if(FAILED(hr)) 
		{
			return S_OK;
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
/// Purpose: To get the system configuration data 
/// Wrapper for GetSystemConfigDataNView-- for use in c#
/// </summary>
/// <param name="dataNView"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSystemConfigDataNViews(/*[in, out]*/IGFX_SYSTEM_CONFIG_DATA_N_VIEWS *dataNView, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		IGFX_SYSTEM_CONFIG_DATA_N_VIEW *pDataNView=(IGFX_SYSTEM_CONFIG_DATA_N_VIEW *)dataNView;
		pDataNView->dwFlags = 1;
		pDataNView->uiSize = sizeof(IGFX_SYSTEM_CONFIG_DATA_N_VIEW);
		hr=GetSystemConfigDataNView(pDataNView,pExtraErrorCode,pErrorDescription);
		pDataNView->dwFlags=0;
		hr=GetSystemConfigDataNView(pDataNView,pExtraErrorCode,pErrorDescription);
		if(FAILED(hr)) 
		{
			return S_OK;
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


STDMETHODIMP CDisplayUtil::GetBezel(/*[in,out]*/ IGFX_BEZEL_CONFIG *pBezelConfig, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_BEZEL_CONFIG_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_BEZEL_CONFIG),(BYTE*)pBezelConfig,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CDisplayUtil::SetBezel(/*[in,out]*/ IGFX_BEZEL_CONFIG *pBezelConfig, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_BEZEL_CONFIG_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_BEZEL_CONFIG),(BYTE*)pBezelConfig,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CDisplayUtil::GetCollageStatus(/*[in,out]*/ IGFX_COLLAGE_STATUS *pCollageStatus, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_COLLAGE_STATUS_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_COLLAGE_STATUS),(BYTE*)pCollageStatus,(DWORD*)pExtraErrorCode);

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

STDMETHODIMP CDisplayUtil::SetCollageStatus(/*[in,out]*/ IGFX_COLLAGE_STATUS *pCollageStatus, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_COLLAGE_STATUS_GUID;

	try
	{		
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_COLLAGE_STATUS),(BYTE*)pCollageStatus,(DWORD*)pExtraErrorCode);

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
/// Purpose: To Get AUX Info
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetAuxInfo(/*[in,out]*/IGFX_AUX_INFO *pAuxInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_AUX_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_AUX_INFO),(BYTE*)pAuxInfo,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To Set AUX Info
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetAuxInfo(/*[in,out]*/IGFX_AUX_INFO *pAuxInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_AUX_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AUX_INFO),(BYTE*)pAuxInfo,(DWORD*)pExtraErrorCode);

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


STDMETHODIMP CDisplayUtil::GetBusInfo(/*[in,out]*/IGFX_BUS_INFO *pBusInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_BUS_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_BUS_INFO),(BYTE*)pBusInfo,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To Set AUX Info
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetBusInfo(/*[in,out]*/IGFX_BUS_INFO *pBusInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_GET_SET_BUS_INFO_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_BUS_INFO),(BYTE*)pBusInfo,(DWORD*)pExtraErrorCode);

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



/// <summary>
/// Purpose: To Get AUX Info
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetSourceHdmiGBDdata(/*[in,out]*/IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_SOURCE_HDMI_GBD_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_SOURCE_HDMI_GBD_DATA),(BYTE*)pSourceHdmiGBDData,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// Purpose: To Set AUX Info
/// </summary>
/// <param name="pVideoQualityEx2"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetSourceHdmiGBDdata(/*[in,out]*/IGFX_SOURCE_HDMI_GBD_DATA *pSourceHdmiGBDData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_SOURCE_HDMI_GBD_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_SOURCE_HDMI_GBD_DATA),(BYTE*)pSourceHdmiGBDData,(DWORD*)pExtraErrorCode);

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

/// <summary>
/// 
/// </summary>
/// <param name="iSize"></param>
/// <param name="pData"></param>
/// <returns></returns>
ULONG checksum(ULONG iSize,PVOID pData)
{
	ULONG sum=0,i=0,*element = (ULONG*)pData;
	ULONG BMUL = iSize & ((ULONG)(-1) - (sizeof(ULONG)-1));
	ULONG NUM = BMUL/sizeof(ULONG);
	for(i=0;i<NUM;i++)
	{
		sum += *(element++);
	}

	return sum;
}

// this function needs to be optimized
HRESULT CDisplayUtil::VistaEscape(int iEsc, int cbIn, void * pIn,/*[out]*/BSTR *pErrorDescription)
{
	PFND3DKMT_ESCAPE				D3DKmtEscape;
	PFND3DKMT_OPENADAPTERFROMHDC	OpenAdapter;
	PFND3DKMT_CLOSEADAPTER			CloseAdapter;

    // input buffer must be prepared by caller
   HRESULT hr = S_OK;

   int retval;

   //
   HMODULE hGdi32 = NULL;
   hGdi32 = LoadLibrary("gdi32.dll");
   if(hGdi32==NULL)
   {
		MessageBox(NULL,"Can't load gdi32.dll","Well,,,,,",0);
		return 0;
   }

   OpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32,"D3DKMTOpenAdapterFromHdc");
   D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32,"D3DKMTEscape");
   CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32,"D3DKMTCloseAdapter");
   // Wrap call into driver in a try block in some vain attempt to catch any
   // exceptions it may generate.

      void * pLocal = NULL;
      HANDLE hLocal = NULL;
	  //HDC hDC = GetDC(NULL);
	  HDC hDC = CreateDC(NULL,"\\\\.\\DISPLAY1",NULL,NULL);
      hLocal = GlobalAlloc(GHND, cbIn);
      retval = -1;
      if (hLocal)
      {
          pLocal = GlobalLock(hLocal);
          if (pLocal)
          {
                memcpy(pLocal, pIn, cbIn);
                SetLastError(0);
                // Call escape function
                GFX_ESCAPE_HEADER_T *pHeader = NULL;

                D3DKMT_OPENADAPTERFROMHDC* poa = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
                ZeroMemory(poa,sizeof(poa));
                poa->hDc = hDC;
                OpenAdapter(poa);

                D3DKMT_ESCAPE esc;
                ZeroMemory(&esc,sizeof(esc));
                esc.hAdapter = poa->hAdapter;
                esc.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
                esc.pPrivateDriverData = (void*)malloc(cbIn+sizeof(GFX_ESCAPE_HEADER_T));
                esc.PrivateDriverDataSize = cbIn+sizeof(GFX_ESCAPE_HEADER_T);

                pHeader = (GFX_ESCAPE_HEADER_T *)malloc(sizeof(GFX_ESCAPE_HEADER_T));
                ZeroMemory(pHeader,sizeof(GFX_ESCAPE_HEADER_T));
                pHeader->EscapeCode =  GFX_ESCAPE_CUICOM_CONTROL;
                pHeader->Size = cbIn;
                pHeader->CheckSum = checksum(cbIn,(PVOID)pLocal);

                memcpy(esc.pPrivateDriverData,pHeader,sizeof(GFX_ESCAPE_HEADER_T));
                char *pPointer = (char*)esc.pPrivateDriverData;
                void *pret = pPointer+sizeof(GFX_ESCAPE_HEADER_T);
                memcpy(pret,pLocal,cbIn);

                ULONG ntret = D3DKmtEscape(&esc);
				
				DeleteDC(hDC);
                if(ntret == 0)
                    retval = 1;
                
                memcpy(pLocal,pret,cbIn);

                //close adapter.
                D3DKMT_CLOSEADAPTER ca;
                ca.hAdapter	 = poa->hAdapter;
                CloseAdapter(&ca);

                //free all the mallocs
                if(pHeader)
                {
                    free(pHeader);
                    pHeader = NULL;
                }
                if(poa)
                {
                    free(poa);
                    poa = NULL;
                }
                if(esc.pPrivateDriverData)
                {
                    free(esc.pPrivateDriverData);
                    esc.pPrivateDriverData =NULL;
                }

                if( retval > 0 ) 
                    memcpy(pIn, pLocal, cbIn);
           }
           GlobalUnlock(hLocal);
       }
       GlobalFree(hLocal);
  
   if (retval > 0)
   {
       hr = S_OK;
	   //MyDebug("\nVista Escape Successful");
   }
   else if (retval == 0)       // Escape call returned 0, Driver does not support this feature.
   {
	   //printf("\nVista Escape Fail:Driver Doesnot support this feature");
	   hr = S_OK;
   }
   else     // Escape call failed.
   {
	   //printf("\nVista Escape Fail: error val = %d",GetLastError());
	   hr = S_OK;
   }
   return(hr);
}


/// <summary>
/// 
/// </summary>
/// <param name="osType"></param>
/// <param name="pAttachedDevices"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetAttachedDevices(/*[in]*/OSTYPE osType,/*[out]*/DWORD *pAttachedDevices,/*[out]*/BSTR *pErrorDescription)
{
	CComBSTR errorStr = L"";
	try
	{
		DWORD dwConnectedDevices = 0;
		COM_DETECT_DEVICE_ARGS detectDeviceBuffer = {0};

		detectDeviceBuffer.ulFlags = ENABLE_CRT_LEGACY_DETECTION | ENABLE_STATIC_DETECTION;
		detectDeviceBuffer.Cmd = COM_DETECT_DEVICE;
		switch(osType)
		{
		case XP:
			{
				HDC hDC = CreateDC(NULL,"\\\\.\\DISPLAY1",NULL,NULL);
				DWORD ret = ExtEscape(hDC,CUICOM_ESCAPE,sizeof(COM_DETECT_DEVICE_ARGS),
					(LPCSTR)&detectDeviceBuffer,sizeof(COM_DETECT_DEVICE_ARGS),(LPSTR)&detectDeviceBuffer);	
				DeleteDC(hDC);
			}
			break;
		default:
			{
				HRESULT hr = VistaEscape(COM_DETECT_DEVICE, sizeof(COM_DETECT_DEVICE_ARGS), &detectDeviceBuffer,pErrorDescription);
				if(FAILED(hr)) 
				{
					return S_OK;
				}
			}
			break;
	
		}
		

		DWORD nDisplays = 0;
		nDisplays=detectDeviceBuffer.DispList.nDisplays;
		for(DWORD index=0;index<nDisplays;index++)
		{
			DWORD dwDisplayUID = detectDeviceBuffer.DispList.ulDisplayUID[index];
			switch(dwDisplayUID)
			{
			case DISPLAYUID_DFP:
				dwConnectedDevices |= DFP;
				break;
			case DISPLAYUID_CRT:
				dwConnectedDevices |= CRT;
				break;
			case DISPLAYUID_TV:
				dwConnectedDevices |= TV;
				break;
			case DISPLAYUID_LFP:
				dwConnectedDevices |= LFP;
				break;

			}
		}

		*pAttachedDevices = dwConnectedDevices;

	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
	}

	return S_OK;
}


/// <summary>
/// To set tri clone
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="dwFlags"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetTriClone(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID,/*[in]*/ DWORD tertiaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID=IGFX_DEVICE_DISPLAYS_GUID_1_0;
	
	try
	{
		
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}
		
		DEVICE_DISPLAYS deviceDisplays={0};
		
		deviceDisplays.nSize = sizeof(DEVICE_DISPLAYS);//size of the display device structure
		deviceDisplays.dwFlags = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_DDCLONE;//single display switch
		deviceDisplays.nMonitors = 2;//no of monitors
		deviceDisplays.monitorIDs[0] = secondaryMonitorID;
		deviceDisplays.monitorIDs[1]=tertiaryMonitorID;
		lstrcpy((TCHAR *)deviceDisplays.strDeviceName,_T("\\\\.\\Display1"));
		deviceDisplays.primaryMonitorID = primaryMonitorID;

		//change the display to given display device
		hr = ptrCUIExternal->ChangeActiveDevices(&structGUID,sizeof(DEVICE_DISPLAYS),(BYTE *)&deviceDisplays,(DWORD*)pExtraErrorCode);
		if(FAILED(hr))
		{
			return S_OK;
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
/// To set tri extended configuration
/// </summary>
/// <param name="primaryMonitorID"></param>
/// <param name="secondaryMonitorID"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::SetTriExtended(/*[in]*/DWORD primaryMonitorID,/*[in]*/ DWORD secondaryMonitorID, DWORD tertiaryMonitorID,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_DEVICE_DISPLAYS_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{
		HRESULT hr=S_OK;

		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}


		DEVICE_DISPLAYS aobjDisp[3] = {0};
		
		for(int nIdx=0 ; nIdx < sizeof(aobjDisp)/sizeof(DEVICE_DISPLAYS) ; nIdx++)
		{
			aobjDisp[nIdx].nSize = sizeof(DEVICE_DISPLAYS);
			aobjDisp[nIdx].nMonitors = 1;
			aobjDisp[nIdx].dwFlags = IGFX_DISPLAY_DEVICE_CONFIG_FLAG_SINGLE;
			aobjDisp[nIdx].primaryMonitorID = 0;
		}
		
		aobjDisp[0].monitorIDs[0] = primaryMonitorID;//primary device
		lstrcpy((TCHAR *)aobjDisp[0].strDeviceName,_T("\\\\.\\Display1"));
		aobjDisp[1].monitorIDs[0] = secondaryMonitorID;//secondary display device
		lstrcpy((TCHAR *)aobjDisp[1].strDeviceName,_T("\\\\.\\Display2"));
		aobjDisp[2].monitorIDs[0] = tertiaryMonitorID;//tertiary display device
		lstrcpy((TCHAR *)aobjDisp[2].strDeviceName,_T("\\\\.\\Display3"));
		
		//set the extended mode
		hr = ptrCUIExternal->ChangeActiveDevices(&structGUID,3*sizeof(DEVICE_DISPLAYS),(BYTE *)aobjDisp,(DWORD *)pExtraErrorCode);
		if(FAILED(hr))
		{
			return S_OK;
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
/// Purpose: To get the gamut expansion data
/// </summary>
/// <param name="customModeList"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetGamutData(/*[in, out]*/IGFX_GAMUT_EXPANSION *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_GAMUT_EXPANSION_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_GAMUT_EXPANSION),(BYTE*)pGamutData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To get the CSC data
/// </summary>
STDMETHODIMP CDisplayUtil::GetCSCData(/*[in, out]*/IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SOURCE_CSC_GUID;
	CComBSTR errorStr = L"";
	try
	{
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			
		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_SOURCE_DISPLAY_CSC_DATA),(BYTE*)pCSCData,(DWORD*)pExtraErrorCode);

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
/// Purpose: To get the CSC data
/// </summary>
STDMETHODIMP CDisplayUtil::SetCSCData(/*[in, out]*/IGFX_SOURCE_DISPLAY_CSC_DATA *pCSCData,
									  /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SOURCE_CSC_GUID;
	CComBSTR errorStr = L"";
	try
	{
		
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));				
		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_SOURCE_DISPLAY_CSC_DATA),(BYTE*)pCSCData,(DWORD*)pExtraErrorCode);

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
/// Purpose: To set the gamut expansion data
/// </summary>
/// <param name="customModeList"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetGamutData(/*[in, out]*/IGFX_GAMUT_EXPANSION *pGamutData, /*[in]*/ float CSCMatrixRow1[3], /*[in]*/ float CSCMatrixRow2[3], /*[in]*/ float CSCMatrixRow3[3], /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_GAMUT_EXPANSION_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));		
			pGamutData->CustomCSCMatrix[0][0]=CSCMatrixRow1[0];
			pGamutData->CustomCSCMatrix[0][1]=CSCMatrixRow1[1];
			pGamutData->CustomCSCMatrix[0][2]=CSCMatrixRow1[2];
			pGamutData->CustomCSCMatrix[1][0]=CSCMatrixRow2[0];
			pGamutData->CustomCSCMatrix[1][1]=CSCMatrixRow2[1];
			pGamutData->CustomCSCMatrix[1][2]=CSCMatrixRow2[2];
			pGamutData->CustomCSCMatrix[2][0]=CSCMatrixRow3[0];
			pGamutData->CustomCSCMatrix[2][1]=CSCMatrixRow3[1];
			pGamutData->CustomCSCMatrix[2][2]=CSCMatrixRow3[2];
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_GAMUT_EXPANSION),(BYTE*)pGamutData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Get the color gamut
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::GetColorGamut(/*[in, out]*/IGFX_GAMUT *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_GAMUT_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_GAMUT),(BYTE*)pGamutData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the color gamut
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetColorGamut(/*[in, out]*/IGFX_GAMUT *pGamutData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_GAMUT_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_GAMUT),(BYTE*)pGamutData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Get the XVYCC
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::GetXvYcc(/*[in, out]*/IGFX_XVYCC_INFO *pXvyccData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_XVYCC_INFO_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_XVYCC_INFO),(BYTE*)pXvyccData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the color gamut
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetXvYcc(/*[in, out]*/IGFX_XVYCC_INFO *pXvyccData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_XVYCC_INFO_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_XVYCC_INFO),(BYTE*)pXvyccData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Get the XVYCC
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::GetYcBcr(/*[in, out]*/IGFX_YCBCR_INFO *pYCBCRData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_YCBCR_INFO_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_YCBCR_INFO),(BYTE*)pYCBCRData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set the color gamut
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>

STDMETHODIMP CDisplayUtil::SetYcBcr(/*[in, out]*/IGFX_YCBCR_INFO *pYCBCRData, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_YCBCR_INFO_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_YCBCR_INFO),(BYTE*)pYCBCRData,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To set Audio Topology
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::SetAudioTopology(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AUDIO_FEATURE_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AUDIO_FEATURE_INFO),(BYTE*)pAudioFeatureInfo,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Get Audio Topology
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::GetAudioTopology(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AUDIO_FEATURE_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_AUDIO_FEATURE_INFO),(BYTE*)pAudioFeatureInfo,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Enable Audio without video
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::EnableAudioWTVideo(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
		HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AUDIO_FEATURE_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AUDIO_FEATURE_INFO),(BYTE*)pAudioFeatureInfo,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// Purpose: To Disable Audio without video
/// </summary>
/// <returns> Success or Failure in pExtraErrorCode </returns>
STDMETHODIMP CDisplayUtil::DisableAudioWTVideo(/*[in, out]*/ IGFX_AUDIO_FEATURE_INFO *pAudioFeatureInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
		HRESULT hr = S_OK;

	GUID structGUID=IGFX_GET_SET_AUDIO_FEATURE_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_AUDIO_FEATURE_INFO),(BYTE*)pAudioFeatureInfo,(DWORD*)pExtraErrorCode);

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
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

/// <summary>
/// 
/// </summary>
/// <param name="pAttachedDevices"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::EnumAttachedDevices(/*[out]*/DWORD *pAttachedDevices,/*[out]*/BSTR *pErrorDescription)
{
	
	DWORD dwDevices=0;
	DWORD uidMonitor;
	HRESULT hr=S_OK;
	int i;
	DWORD dwDeviceType;
	DWORD dwStatus;
	CComBSTR errorStr = L"";
	
	CComBSTR strDeviceName = L"\\\\.\\Display1";
	try
	{
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
	i=0;
	hr=S_OK;
	while(hr==S_OK)
	{
		try
		{
			hr=ptrCUIExternal->EnumAttachableDevices(strDeviceName.m_str,i,&uidMonitor,&dwDeviceType,&dwStatus);
			
			switch(dwDeviceType)
			{
			case IGFX_CRT:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=CRT;
				break;
			case IGFX_LocalFP:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=LFP;
				break;
			case IGFX_ExternalFP:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=DFP;
				break;
			case IGFX_TV:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=TV;
				break;
			case IGFX_NULL_DEVICE:
			default:
				dwDevices|=0;
				break;
			}
			i++;
		}
		catch(...)
		{
			hr = E_FAIL;			
		}
	}
	
	strDeviceName = L"\\\\.\\Display2";
	i=0;
	hr=S_OK;
	while(hr==S_OK)
	{
		try
		{
			hr=ptrCUIExternal->EnumAttachableDevices(strDeviceName.m_str,i,&uidMonitor,&dwDeviceType,&dwStatus);
			
			switch(dwDeviceType)
			{
			case IGFX_CRT:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=CRT;
				break;
			case IGFX_LocalFP:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=LFP;
				break;
			case IGFX_ExternalFP:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=DFP;
				break;
			case IGFX_TV:
				if(IGFX_DISPLAY_DEVICE_ALL&dwStatus)
					dwDevices|=TV;
				break;
			case IGFX_NULL_DEVICE:
			default:
				dwDevices|=0;
				break;
			}
			i++;
		}
		catch(...)
		{
			hr = E_FAIL;
		}		
	}
	hr=S_OK;
	
	*pAttachedDevices = dwDevices;
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

	return S_OK;
}

/// <summary>
/// Dummy Function so that the data sturctures are visible outside COM
/// </summary>
STDMETHODIMP CDisplayUtil::DummyFunction(DISPLAY_RELATED *pDisplayRelated,OPERATING_MODE *pOperatingMode,NEW_DEVICE_TYPE *pDeviceType,DISPLAY_DEVICE_STATUS *pDisplayDeviceStatus,IGFX_DISPLAY_TYPES *pDisplayTypes,GENERIC *pGeneric,IGFX_MEDIA_FEATURE_TYPES *pMediaFeatureTypes,
										IGFX_COLOR_QUALITIES *pColorQualities,IGFX_TIMING_STANDARDS *pTimingStandards,IGFX_CUSTOM_MODES *pCustomModes,  IGFX_DISPLAY_RESOLUTION_EX *Resolution,IGFX_DISPLAY_POSITION *Position,REFRESHRATE *pRefreshRate,DISPLAY_CONFIG_CODES *pDisplayConfigCodes,
										DISPLAY_ORIENTATION *pDisplayOrientation, MEDIA_GAMUT_COMPRESSION_VALUES *pMediaGamutCompressionValues)
{
	return S_OK;
}

/// <summary>
/// 
/// </summary>
/// <param name="pDeviceDisplays"></param>
/// <param name="pExtraErrorCode"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
STDMETHODIMP CDisplayUtil::GetCurrentConfig(DEVICE_DISPLAYS *pDeviceDisplays, IGFX_ERROR_CODES *pExtraErrorCode, BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";
	try
	{
		GUID structGUID = IGFX_CURRENT_CONFIG_GUID ;
		//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			
			return hr;
		}

		
		hr = ptrCUIExternal->GetConfiguration(&structGUID,sizeof(DEVICE_DISPLAYS),(BYTE *)pDeviceDisplays,(DWORD*)pExtraErrorCode);
		if(FAILED(hr))
		{
			errorStr = L"E_FAIL";
			*pErrorDescription=errorStr.Copy();
			return S_OK;
		}

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
	return S_OK;
}


STDMETHODIMP CDisplayUtil::GetGOPVersion(/*[in, out]*/IGFX_GOP_VERSION *pGopVersion, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_GOP_VERSION_GUID;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_GOP_VERSION),(BYTE*)pGopVersion,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

STDMETHODIMP CDisplayUtil::GetChipSetInformation(/*[in, out]*/DWORD *pChipsetInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID=IGFX_SYSTEM_INFO_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(DWORD),(BYTE*)pChipsetInfo,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

STDMETHODIMP CDisplayUtil::GetDisplayInformation(/*[in, out]*/DWORD *pDisplayInfo, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;

	GUID structGUID = IGFX_DISPLAY_DATA_GUID_1_0;
	CComBSTR errorStr = L"";
	try
	{
		{
			
			hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(DWORD),(BYTE*)pDisplayInfo,(DWORD*)pExtraErrorCode);

			if(FAILED(hr)) 
			{
					
				return S_OK;

			}
		}
	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";*pErrorDescription=errorStr.Copy();
//		*pBuffer = errorDesc.Copy();
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;
}

STDMETHODIMP CDisplayUtil::SetGraphcisRestoreDefault(/*[in,out]*/IGFX_RESTORE_GRAPHICS_DEFAULT_INFO *pGraphicsRestoreDefault, /*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	GUID structGUID = IGFX_SET_RESTORE_GRAPHICS_DEFAULT_GUID;

	try
	{		
		{
			//ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
			
			hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_RESTORE_GRAPHICS_DEFAULT_INFO),(BYTE*)pGraphicsRestoreDefault,(DWORD*)pExtraErrorCode);

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

#define szEnableNLAS				_T("EnableNLAS")
#define szNLASVerticalCrop			_T("NLASVerticalCrop")
#define szNLASHLinearRegion			_T("NLASHLinearRegion")
#define szNLASNonLinearCrop			_T("NLASNonLinearCrop")
#define szMediaValues    "Software\\Intel\\Display\\igfxcui\\Media"	

STDMETHODIMP CDisplayUtil::ReadRegistryEnableNLAS(DWORD *regvalue)
{
	HRESULT hr = S_OK;
	HKEY hKey = NULL;
	DWORD dwRetVal = RegOpenKey(HKEY_CURRENT_USER, szMediaValues, &hKey);	
	DWORD dwSize = sizeof(DWORD),dwType = 0, dwVal=0;	
	RegQueryValueEx(hKey,szEnableNLAS,NULL,&dwType,(BYTE *)&dwVal,&dwSize);	
	*regvalue = dwVal;
	RegCloseKey(hKey);
	return hr;
}

STDMETHODIMP CDisplayUtil::ReadRegistryNLASVerticalCrop(float *regvalue)
{
	HRESULT hr = S_OK;
	HKEY hKey = NULL;
	DWORD dwRetVal = RegOpenKey(HKEY_CURRENT_USER, szMediaValues, &hKey);	
	DWORD dwSize = sizeof(DWORD),dwType = 0, dwVal=0;
	PFLOAT pfVal=NULL;
	RegQueryValueEx(hKey,szNLASVerticalCrop,NULL,&dwType,(BYTE *)&dwVal,&dwSize);
	pfVal = (PFLOAT)&dwVal;
	*regvalue = (*pfVal);
	RegCloseKey(hKey);
	return hr;
}

STDMETHODIMP CDisplayUtil::ReadRegistryNLASHLinearRegion(float *regvalue)
{
	HRESULT hr = S_OK;
	HKEY hKey = NULL;
	DWORD dwRetVal = RegOpenKey(HKEY_CURRENT_USER, szMediaValues, &hKey);	
	DWORD dwSize = sizeof(DWORD),dwType = 0, dwVal=0;
	PFLOAT pfVal=NULL;
	RegQueryValueEx(hKey,szNLASHLinearRegion,NULL,&dwType,(BYTE *)&dwVal,&dwSize);
	pfVal = (PFLOAT)&dwVal;
	*regvalue = (*pfVal);
	RegCloseKey(hKey);
	return hr;
}

STDMETHODIMP CDisplayUtil::ReadRegistryNLASNonLinearCrop(float *regvalue)
{
	HRESULT hr = S_OK;
	HKEY hKey = NULL;
	DWORD dwRetVal = RegOpenKey(HKEY_CURRENT_USER, szMediaValues, &hKey);	
	DWORD dwSize = sizeof(DWORD),dwType = 0, dwVal=0;
	PFLOAT pfVal=NULL;
	RegQueryValueEx(hKey,szNLASNonLinearCrop,NULL,&dwType,(BYTE *)&dwVal,&dwSize);
	pfVal = (PFLOAT)&dwVal;
	*regvalue = (*pfVal);
	RegCloseKey(hKey);
	return hr;
}

///

//HRESULT CDisplayUtil::ErrorHandler2(/*[in]*/BSTR functionName,/*[out]*/BSTR *pErrorDescription)
/*
{
	USES_CONVERSION;
	TCHAR szBuf[80]; 
	LPVOID lpMsgBuf;
	DWORD dw = GetLastError(); 

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
				NULL,dw, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
				(LPTSTR) &lpMsgBuf,0, NULL );
    wsprintf(szBuf, "%s failed with error %d: %s", OLE2T(functionName), dw, lpMsgBuf); 
    LocalFree(lpMsgBuf);
	*pErrorDescription = T2OLE(szBuf);

	return S_OK;
}
*/

/// <summary>
/// 
/// </summary>
/// <param name="functionName"></param>
/// <param name="hr"></param>
/// <param name="pErrorDescription"></param>
/// <returns></returns>
HRESULT CDisplayUtil::ErrorHandler(/*[in]*/BSTR functionName,/*[in]*/HRESULT hr,/*[out]*/BSTR *pErrorDescription)
{
	USES_CONVERSION;
	CComBSTR errorStr = functionName;
	try
	{
		USES_CONVERSION;
		TCHAR szBuf[80]; 
		LPVOID lpMsgBuf;

		FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
				NULL,hr, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
				(LPTSTR) &lpMsgBuf,0, NULL );
		wsprintf(szBuf, "%s failed with error %s", OLE2T(functionName), lpMsgBuf); 
		LocalFree(lpMsgBuf);
		*pErrorDescription = T2OLE(szBuf);
		errorStr.Append(" ");
		errorStr.Append(T2OLE(szBuf));
		*pErrorDescription = errorStr.Copy();
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
	return S_OK;
}

//STDMETHODIMP CDisplayUtil::EnumExtendedDesktopDisplaySettings(DISPLAY_MODE *pDisplay1Mode,DISPLAY_MODE *pDisplay2Mode,BSTR *pErrorDescription)
/*
{
	USES_CONVERSION;
	CComBSTR errorStr = L"";

	DEVMODE devMode1 = {0};
	devMode1.dmSize = sizeof(DEVMODE);
	devMode1.dmFields = DM_POSITION | DM_COLOR | DM_YRESOLUTION | DM_BITSPERPEL	|
						DM_PELSWIDTH| DM_PELSHEIGHT | DM_DISPLAYFREQUENCY;
	BOOL bRetVal = EnumDisplaySettingsEx(
	  "\\\\.\\DISPLAY1",  // display device
	  ENUM_CURRENT_SETTINGS,          // graphics mode
	  &devMode1,      // graphics mode settings
	  EDS_RAWMODE            // options
	);

	if(bRetVal == 0)
	{
		return ErrorHandler2(L"EnumDisplaySettingsEx",pErrorDescription);		
	}

	
		
	(*pDisplay1Mode).vmHzRes=devMode1.dmPelsWidth;
	(*pDisplay1Mode).vmVtRes=devMode1.dmPelsHeight;
	(*pDisplay1Mode).vmPixelDepth=devMode1.dmBitsPerPel;
	(*pDisplay1Mode).vmRefreshRate=devMode1.dmDisplayFrequency;
	
	DEVMODE devMode2 = {0};
	devMode2.dmSize = sizeof(DEVMODE);
	devMode2.dmFields = 
			DM_POSITION | DM_COLOR | DM_YRESOLUTION | DM_BITSPERPEL | 
			DM_PELSWIDTH|DM_PELSHEIGHT|DM_DISPLAYFREQUENCY;
	
	bRetVal = EnumDisplaySettingsEx(
	  "\\\\.\\DISPLAY2",  // display device
	  ENUM_CURRENT_SETTINGS,          // graphics mode
	  &devMode2,      // graphics mode settings
	  EDS_RAWMODE            // options
	);
	
	(*pDisplay2Mode).vmHzRes=devMode2.dmPelsWidth;
	(*pDisplay2Mode).vmVtRes=devMode2.dmPelsHeight;
	(*pDisplay2Mode).vmPixelDepth=devMode2.dmBitsPerPel;
	(*pDisplay2Mode).vmRefreshRate=devMode2.dmDisplayFrequency;

	if(bRetVal == 0)
	{
		return ErrorHandler2(L"EnumDisplaySettingsEx",pErrorDescription);		
	}


	return S_OK;
}
*/

STDMETHODIMP CDisplayUtil::IsWOW64(BOOL *pIsWOW64, BSTR *pErrorDescription)
{
    BOOL bIsWOW64 = FALSE;

    fnIsWow64Process = (LPFN_ISWOW64PROCESS)GetProcAddress(
        GetModuleHandle(TEXT("kernel32")),"IsWow64Process");
  
    if (NULL != fnIsWow64Process)
    {
        if (!fnIsWow64Process(GetCurrentProcess(),&bIsWOW64))
        {
            *pErrorDescription = L"Failed to find whether process is using in 64";
			*pIsWOW64 = false;
			return S_OK;

        }
    }

	*pIsWOW64 = bIsWOW64;

	return S_OK;
}


STDMETHODIMP CDisplayUtil::DoEscape(OSTYPE osType,BSTR *pKeyName, BSTR *pErrorDescription)
{
	CComBSTR errorStr = L"";
	try
	{
		COM_CUIREGISTRY_DWORD_ARGS escpGetRegistry = {0};
		escpGetRegistry.Action = GET_REG_VALUE;
		escpGetRegistry.Cmd    = COM_CUI_REGISTRY_DWORD;
		wcscpy(escpGetRegistry.pwszValueName, *pKeyName);

	
		switch(osType)
		{
		case XP:
			{
				HDC hDC = CreateDC(NULL,"\\\\.\\DISPLAY1",NULL,NULL);
				DWORD retVal = ExtEscape(hDC,CUICOM_ESCAPE,sizeof(COM_CUIREGISTRY_DWORD_ARGS),
					(LPCSTR)&escpGetRegistry,sizeof(COM_CUIREGISTRY_DWORD_ARGS),(LPSTR)&escpGetRegistry);	
				DeleteDC(hDC);

				if(retVal > 0)
				{
					errorStr = L"Ext Escape Call Succeeded";
					*pErrorDescription=errorStr.Copy();
				}
				else
				{
					errorStr = L"Ext Escape Call failed";
					*pErrorDescription=errorStr.Copy();
				}
			}
			break;
		case VISTA:
			{
				HRESULT hr = VistaEscape(COM_CUI_REGISTRY_DWORD, sizeof(COM_CUIREGISTRY_DWORD_ARGS), &escpGetRegistry,pErrorDescription);
				if(FAILED(hr)) 
				{
					return S_OK;
				}
			}
			break;
		}
		
	}
	catch(...)
	{
		errorStr = L"Unknown Error";
		*pErrorDescription=errorStr.Copy();
	}

	return S_OK;
}

