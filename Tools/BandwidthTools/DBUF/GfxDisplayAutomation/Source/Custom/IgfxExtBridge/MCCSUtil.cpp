// MCCSUtil.cpp : Implementation of CMCCSUtil
#include "stdafx.h"
#include "IgfxExtBridge.h"
#include "MCCSUtil.h"
#include "Guids.h"
#include <stdio.h>
#include <tchar.h>
#include <math.h>
#include "UserStructs.h"
#include "mccsconsts.h"


ICUIDriverPtr  CMCCSUtil::ptrCUIDriver;
ICUIExternal8Ptr CMCCSUtil::ptrCUIExternal;

UINT CMCCSUtil::mccsUtilHandle = 0;
CMCCSUtil::CMCCSUtil()
{
	HRESULT hr = E_FAIL;
	if(ptrCUIExternal == NULL)
	{
		hr = ptrCUIExternal.CreateInstance(CLSID_CUIExternal,NULL);
		if(hr != S_OK)
		{
			//log it
		}
		
	}

	if(ptrCUIDriver == NULL)
	{
		hr = ptrCUIDriver.CreateInstance(CLSID_CUIDriver,NULL);
		if(hr != S_OK)
		{
			//log it
		}
	}
}

/*
CMCCSUtil::~CMCCSUtil()
{
	
	if(ptrCUIExternal != NULL)
	{
	ptrCUIExternal.Release();
	}

	if(ptrCUIDriver != NULL)
	{
		ptrCUIDriver.Release();
	}
}
	
*/

/// <summary>
/// Opens the MCCS interface, and stores the handles in a  class variable.
/// </summary>
/// <param name="monitorID"></param>
/// <param name="pHandle"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Open(/*[in]*/DWORD monitorID,/*[out]*/DWORD *pHandle,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription) 		
{
	HRESULT hr=S_OK;
	GUID structGUID;
	structGUID = IGFX_MCCS_GUID_1_0;
	IGFX_MCCS_DATA mccsdata = {0};
	CComBSTR errorStr = L"";

	try
	{	
		mccsdata.dwDevice = monitorID;
		mccsdata.Cmd = MCCS_OPEN;

	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));	
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}

		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MCCS_DATA),(BYTE*)&mccsdata,(DWORD*)pExtraErrorCode);
	
		if (SUCCEEDED(hr) && (*pExtraErrorCode) == IGFX_SUCCESS)
		{			     
			*pHandle = mccsdata.uiHandle;  		
			mccsUtilHandle = mccsdata.uiHandle;  		
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
		*pExtraErrorCode = UNKNOWN_ERROR;	
	}

	return hr;

 
}

/// <summary>
/// Closes the MCCS interface, and removes the handles from local variables.
/// </summary>
/// <param name="dwHandle"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Close(/*[in]*/DWORD dwHandle,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";
	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
	
		hr = ptrCUIExternal->MccsClose(dwHandle);

		mccsUtilHandle = 0;
		ptrCUIExternal.Release();		
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
/// Returns the maximum value of the particular control code.
/// </summary>
/// <param name="dwHandle"></param>
/// <param name="controlCode"></param>
/// <param name="size"></param>
/// <param name="pVal"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Max(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
    CComBSTR errorStr = L"";
	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		} 		
	 
		hr = ptrCUIExternal->MccsGetMax(dwHandle,controlCode,size,pVal,(DWORD *)pExtraErrorCode) ;

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	 
	}

	return hr;
}


/// <summary>
/// Returns the Minimum value of the particular control code.
/// </summary>
/// <param name="dwHandle"></param>
/// <param name="controlCode"></param>
/// <param name="size"></param>
/// <param name="pVal"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Min(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}

		hr = ptrCUIExternal->MccsGetMin(dwHandle,controlCode,size,pVal,(DWORD *)pExtraErrorCode) ;

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	 
	}

	return hr;
}

/// <summary>
/// Resets a particular control with default value.
/// </summary>
/// <param name="dwHandle"></param>
/// <param name="controlCode"></param>
/// <param name="size"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::ResetControl(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
		 
		hr = ptrCUIExternal->MccsResetControl(dwHandle,controlCode,size,(DWORD *)pExtraErrorCode);

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	 
	}

	return hr;
}

/// <summary>
/// Returns the Current value of a particular control code.
/// </summary>
/// <param name="dwHandle"></param>
/// <param name="controlCode"></param>
/// <param name="size"></param>
/// <param name="pVal"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::GetCurrent(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in,out]*/DWORD *pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
		
		hr = ptrCUIExternal->MccsGetCurrent(dwHandle,controlCode,size,pVal,(DWORD *)pExtraErrorCode) ;


	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	 
	}

	return hr;
}

/// <summary>
/// Sets a value for the particular control code.
/// </summary>
/// <param name="dwHandle"></param>
/// <param name="controlCode"></param>
/// <param name="size"></param>
/// <param name="pVal"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>      
STDMETHODIMP CMCCSUtil::SetCurrent(/*[in]*/DWORD dwHandle,/*[in]*/DWORD controlCode,/*[in]*/DWORD size,/*[in]*/DWORD pVal,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}
		
		hr = ptrCUIExternal->MccsSetCurrent(dwHandle,controlCode,size,pVal,(DWORD *)pExtraErrorCode) ;	

	}
	catch(_com_error& error)
	{
		errorStr = error.ErrorMessage();
		*pErrorDescription=errorStr.Copy();
		//*pExtraErrorCode = IGFX_REGISTRATION_ERROR;
	}
	catch(...)
	{
		*pExtraErrorCode = UNKNOWN_ERROR;	 
	}

	return hr;
}

inline unsigned short GET_HEX_NUM(short x)		
{
	unsigned short nNum = 0;
	if ( (x >= _T('0')) && (x <= _T('9')) )
		nNum = x - _T('0');
	else
	if ( (x >= _T('A')) && (x <= _T('F')) )
		nNum = x - _T('A') + 10;	// Because  10 is hex A, 11 is B and so on.
	else
	if ( (x >= _T('a')) && (x <= _T('f')) )
		nNum = x - _T('a') + 10;	// Because  10 is hex a, 11 is b and so on.
	
	return nNum;
}


inline unsigned short GetCommand(char cHighByte,char cLowByte)
{
	unsigned short unOpCode;
	
	unOpCode = 16 * GET_HEX_NUM(cHighByte);  // radix 16 for hexadecimal
	unOpCode += GET_HEX_NUM(cLowByte);

	return unOpCode;

}

/// <summary>
/// 
/// </summary>
/// <param name="pCapabilities"></param>
/// <param name="pCmdArray"></param>
/// <param name="pTotalCmds"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::ParseCapabilityCmds(/*[in]*/BSTR *pCapabilities,/*[in]*/DWORD *pCmdArray,/*[out]*/DWORD *pTotalCmds,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	CComBSTR errorStr = L"";

	static BYTE szCapability[9000];
	bool bBreakLoop = false;
	char* szToken;
	unsigned short unOpCode;
	int nIndex=0;

	
	try
	{	
		strcpy((char *)szCapability ,(char *)pCapabilities);
		szToken = strtok((char*)szCapability,_T(" ,()\t\n"));
	 
		if (NULL == pCapabilities)
		{
			return S_OK;
		}
		
		while(true != bBreakLoop)
		{
			if ((!stricmp(szToken, _T("cmds"))))
			{
				szToken = strtok(NULL,_T(")\t\n"));
					
				int index=0;
			 
				while(*(szToken+index) != _T('\0'))
				{
					if (NULL == _tcschr( _T("\n \t\r"), int(*(szToken+index))))
					{
						unOpCode = GetCommand(*(szToken+index),*(szToken+index+1));
						pCmdArray[nIndex++]=unOpCode; 
					}
					index+=2;
				}
			}
			else
			{
				szToken = strtok(NULL,_T(" ,()\t\n"));
				if(NULL == szToken)
					bBreakLoop = true;
			}
		}

		*pTotalCmds = nIndex;

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
/// <param name="pCapabilities"></param>
/// <param name="pVcpArray"></param>
/// <param name="pTotalCmds"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::ParseCapabilityVCP(/*[in]*/BSTR *pCapabilities,/*[in]*/DWORD *pVcpArray,/*[out]*/DWORD *pTotalCmds,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	bool bBreakLoop = false;
	char* szToken;
	unsigned short unOpCode;
	int nIndex=0;
	CComBSTR errorStr = L"";

	try
	{	
	 	if (NULL == pCapabilities)
		{
			return S_OK;
		}


		szToken = strtok((char*)pCapabilities,_T(" ,()\t\n"));

		while(true != bBreakLoop)
		{
			if ((!_tcsicmp(szToken, _T("vcp"))))  // level 2 keyword
			{
				szToken = strtok(NULL,_T(")\t\n"));

				int index =0;

				while(*(szToken+index) != _T('\0'))
				{
					if (NULL == _tcschr( _T("\n \t\r"), int(*(szToken+index))))
					{
						unOpCode = GetCommand(*(szToken+index),*(szToken+index+1));
						pVcpArray[nIndex++] = unOpCode;
					}	

					index+=2;
				}
			}
			else
			{
				szToken = strtok(NULL,_T(" ,()\t\n"));
				if(NULL == szToken)
					bBreakLoop = true;
			}
		
		}

		*pTotalCmds = nIndex;
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
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Get(/*[in,out]*/IGFX_MCCS_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;

	GUID structGUID;
	structGUID = IGFX_MCCS_GUID_1_0;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}

		if(pBuffer->Cmd == MCCS_OPEN && mccsUtilHandle != 0)
		{
			Close(mccsUtilHandle,pErrorDescription);			
			ptrCUIExternal.CreateInstance(CLSID_CUIExternal,NULL);
		}
	

		hr=ptrCUIExternal->GetDeviceData(&structGUID,sizeof(IGFX_MCCS_DATA),(BYTE*)pBuffer,(DWORD *)pExtraErrorCode);		

		
		if(pBuffer->Cmd == MCCS_OPEN)
		{
			mccsUtilHandle = pBuffer->uiHandle;
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
/// <param name="pBuffer"></param>
/// <param name="pExtraErrorCode"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::Set(/*[in,out]*/IGFX_MCCS_DATA *pBuffer,/*[out]*/IGFX_ERROR_CODES *pExtraErrorCode,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr=S_OK;
	GUID structGUID;
	structGUID = IGFX_MCCS_GUID_1_0;
	CComBSTR errorStr = L"";

	try
	{	
	 //	ICUIExternal8Ptr ptrCUIExternal(__uuidof(CUIExternal));
		if(ptrCUIExternal == NULL)
		{
			return S_OK;
		}

		hr=ptrCUIExternal->SetDeviceData(&structGUID,sizeof(IGFX_MCCS_DATA),(BYTE*)pBuffer,(DWORD *)pExtraErrorCode);		

		if(pBuffer->Cmd == MCCS_CLOSE)
		{
			mccsUtilHandle = 0;
			ptrCUIExternal.Release();
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
/// <param name="pCapability"></param>
/// <param name="pSize"></param>
/// <returns></returns>
STDMETHODIMP CMCCSUtil::GetCapability(/*in*/DWORD monitorID,/*out*/BSTR *pCapability,/*out*/DWORD *pSize,/*[out]*/BSTR *pErrorDescription)
{
	HRESULT hr = S_OK;
	CComBSTR errorStr = L"";

	try
	{
		char* strValue = new char[*pSize];
	    //char* strValue = _com_util::ConvertBSTRToString(*pCapability);
		unsigned char* pCapString= (unsigned char*)strValue;
		*pCapString = '\0';
	
		CUII2C_WERROR* pcui2c = new CUII2C_WERROR;
		WORD wOffSet = 0x0000, wBlkLgth=0;
		int  nCapStrSize = 0;
			

	
		if(ptrCUIDriver == NULL)
		{
			return S_OK;
		}

		
		if(monitorID == 0)
		{
			monitorID = 1;
		}
	

		for(BYTE bIndex=0; ; wOffSet+=wBlkLgth, bIndex++)
		{
			::ZeroMemory(pcui2c,sizeof(CUII2C_WERROR));
				
			((CUII2C_WERROR *)pcui2c)->Value.bus = DDCBUS;
			((CUII2C_WERROR *)pcui2c)->Value.dev = AB_DEVICE_ADDR;
			((CUII2C_WERROR *)pcui2c)->Value.SubAddr = AB_HOST_ADDR;
			((CUII2C_WERROR *)pcui2c)->Value.dwFlags = i2cf_Init | i2cf_DevValid;
			((CUII2C_WERROR *)pcui2c)->dwDevice = monitorID;
			
			CUII2C* pCUII2C  =  static_cast<CUII2C*> (&(((CUII2C_WERROR *)pcui2c)->Value));
			pCUII2C->bData[0] = AB_GETCAP_LEN_BYTE;	// Protocol + len
			pCUII2C->bData[1] = AB_GETCAP_OPCODE;	// Get-Cap feature op code
			pCUII2C->bData[2] = HIBYTE(wOffSet);	// offset
			pCUII2C->bData[3] = LOBYTE(wOffSet);	// offset
			pCUII2C->dwWriteBytes = 1 + AB_GET_ABMSG_LEN(pCUII2C->bData[0]);
			pCUII2C->dwReadBytes = AB_CAP_REPLY_LEN;

			GUID AtomicI2CGUID = AtomicI2C;
		
			hr = ptrCUIDriver->GetDeviceData(&AtomicI2CGUID,sizeof(CUII2C_WERROR),(BYTE*)pcui2c);

			if (S_OK != hr)
			{
				break;
			}

			if (AB_DEVICE_ADDR == (pCUII2C->bData[0]))			// check if first byte is access bus addr
			{
				wBlkLgth = AB_GET_ABMSG_LEN(pCUII2C->bData[1]) ;	// get msg len from second byte
						
				//Bug 1183844 - Jay
				//If wBlkLgnth = 0, creates a problem when you subtract 3 from it. 
				if(wBlkLgth >= 3)	//Hence need to change this part of the code to fix it.
				{
					wBlkLgth -= 3;	// subtract 3 bytes for (one opcode byte and 2 offset bytes)
				}
				//End of Bug 1183844

				// if Cap block length is zero, stop calling the Cap String retrieval function
				if (0 >= wBlkLgth)	
				{
					break;
				}
			}
			else
			{
				// if the device address is not correct, break out.
				// this is required because if a monitor does not support DDC2Bi protocol
				// we must break here.
				hr = E_NOTSUPPORTED;
				break;	
			}

			// overflow watchdog. If cap string exceeds 200 segments, stop it.
			// The above comment is taken from the VESA DDC/CI Standard sample code on page 41
			if (200 <= bIndex)
				break;
					
			int index;
			for(index=0; index < (AB_GET_ABMSG_LEN(pCUII2C->bData[1])-3); index++)
			{
				// move by 5 positions to skip 5 bytes (dev addr byte, len byte, op code byte and 2 offset bytes)
				if (0 == pCUII2C->bData[5+index]) // value 0 indicates end of capstring data
					break;

				pCapString[nCapStrSize] = pCUII2C->bData[5+index];
				nCapStrSize++;	
			}
		}

		pCapString[nCapStrSize] = 0;
		*pCapability = _com_util::ConvertStringToBSTR(strValue);

		*pSize	= nCapStrSize;
		delete pcui2c;

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


