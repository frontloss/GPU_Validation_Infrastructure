/*******************************************************************************
**
** Copyright (c) Intel Corporation (2012).
**
** DISCLAIMER OF WARRANTY
** NEITHER INTEL NOR ITS SUPPLIERS MAKE ANY REPRESENTATION OR WARRANTY OR
** CONDITION OF ANY KIND WHETHER EXPRESS OR IMPLIED (EITHER IN FACT OR BY
** OPERATION OF LAW) WITH RESPECT TO THE SOURCE CODE.  INTEL AND ITS SUPPLIERS
** EXPRESSLY DISCLAIM ALL WARRANTIES OR CONDITIONS OF MERCHANTABILITY OR
** FITNESS FOR A PARTICULAR PURPOSE.  INTEL AND ITS SUPPLIERS DO NOT WARRANT
** THAT THE SOURCE CODE IS ERROR-FREE OR THAT OPERATION OF THE SOURCE CODE WILL
** BE SECURE OR UNINTERRUPTED AND HEREBY DISCLAIM ANY AND ALL LIABILITY ON
** ACCOUNT THEREOF.  THERE IS ALSO NO IMPLIED WARRANTY OF NON-INFRINGEMENT.
** SOURCE CODE IS LICENSED TO LICENSEE ON AN 'AS IS' BASIS AND NEITHER INTEL
** NOR ITS SUPPLIERS WILL PROVIDE ANY SUPPORT, ASSISTANCE, INSTALLATION,
** TRAINING OR OTHER SERVICES.  INTEL AND ITS SUPPLIERS WILL NOT PROVIDE ANY
** UPDATES, ENHANCEMENTS OR EXTENSIONS.
**
** File Name: PerfProfile.cpp
**
** Description: Contains function definitions used by the PerfProfile.dll
**
** Author : Shreyansh Sinha ( 4/10/2012 )
**
*******************************************************************************/
#include "stdafx.h"
#include "windows.h"
#include "PerfProfile.h"
#include "GfxPerfEvents.h"
#include "GfxPerfFunctions.h"
#include "Event_Profiling.h"
#include "gfxEscape.h"
#include "stdio.h"
#include  "malloc.h"
#include  <stdlib.h>
#include <strsafe.h>
// FOR D3DKmtEsc

HMODULE hGdi32 = NULL;
PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter = NULL;
PFND3DKMT_ESCAPE D3DKmtEscape = NULL;
PFND3DKMT_CLOSEADAPTER CloseAdapter = NULL;
PFND3DKMT_INVALIDATEACTIVEVIDPN InvalidateActiveVidPnThunk = NULL;

int DumpData(PEVENT_PROFILING_INFO pEventProfileInfo,FILE* LogFile );

/***********************************************************************************

	Function Name : GfxInitProfiling ()

	IN Paramters : ulVersionNumber 

    Purpose : Function to send the version number to the dll .If any mismatch return
              error

    Return Value: E_FAIL - Incase of Error
	              
				  S_OK -   Incase of Success

************************************************************************************/
HRESULT  GfxInitProfiling( ULONG ulVersionNumber)
{
   HRESULT hr = E_FAIL;

   if( PROFILING_VERSION_NUMBER != ulVersionNumber )
   {
	   printf("Version Mismatch\n DLL Version is %d",PROFILING_VERSION_NUMBER);
	   return hr;
   }
      
   return S_OK ;
}


/***********************************************************************************

	Function Name : GfxStartProfiling ()

	IN Paramters : 1.EventName - event to be profiled
	                
				   2.bUseAppDependencyData - True - use app dependency data

											 False - driver to use it's own
											         dependency data

				   3.pDependencyData - User provided dependency data. Should be Null
				                       if bUseAppDependencyData is False

    Purpose : Function to send the escape call to driver to start the event profiling

	Return Value: E_FAIL - Incase of Error
	              
				  S_OK -   Incase of Success

************************************************************************************/

HRESULT __cdecl GfxStartProfiling(EVENT_NAME_PROFILING EventName ,bool bUseAppDependencyData , PDEPENDENCY_DDI_PROFILING pDependencyData)
{
   HRESULT hr = E_FAIL;
   
   // do the version checking 
   hr = GfxInitProfiling(1);
   if ( E_FAIL == hr)
   {
	   return hr;
   }
   else 
   {
   //Allocate Memory for the Escape structure

   PEVENT_PROFILING_START_ARGS pStartPerf = (PEVENT_PROFILING_START_ARGS)malloc(sizeof (EVENT_PROFILING_START_ARGS)) ;

   ZeroMemory(pStartPerf, sizeof(EVENT_PROFILING_START_ARGS));

   // Fill the Escape structure

   pStartPerf->ulCmd = EVENT_PROFILING_ESC_START_ARGS ;
   pStartPerf->eEventForProfiling = EventName;
   pStartPerf->bUseAppDependencyData = bUseAppDependencyData ;

   // Advanced user will have the option to give the dependency data for the event 
	   
   if (true == bUseAppDependencyData)
   {
		if (pDependencyData)
		{
			pStartPerf->stDependencyData = *pDependencyData ;
		}
		else
		{
			MessageBox(NULL,TEXT("The dependency data is not provided by the user"),TEXT("Perfomance Tool"), MB_OK);
			free(pStartPerf);
			return hr ;
		 }
	}

   // Call the Escape Wrapper Function 

   hr = DoEsc( (LPCSTR)pStartPerf , sizeof (EVENT_PROFILING_START_ARGS), NULL , 0);
   if(E_FAIL == hr)
   {
	    printf("start escape returned failure \n");

   }
   free(pStartPerf);
	   
   return hr;
   }
}


/***********************************************************************************

	Function Name : GfxStopProfiling ()

	IN Paramters : EventName

    Purpose : 1. Function will send the STOP escape call to the driver. This will signal 
			     the driver to stop profiling.
               
              2. Function will call GfxCreateLog() to create the log files

			  3. Function will call GfxCleanup() to make the escape call to driver
			     to ask the driver to cleanup its variables and reset the registry
    
	Return Value: E_FAIL - Incase of Error
	              
				  S_OK -   Incase of Success

************************************************************************************/

HRESULT __cdecl GfxStopProfiling(EVENT_NAME_PROFILING EventName , FILE* LogFile )
{
   DWORD lresult = 0;
   HRESULT hr = E_FAIL;
   if (EventName != CUSTOM_EVENT)
   {
	   if (FALSE == IsEventProfilingComplete())
		   return E_FAIL;
   }

   //allocate memory for stop escape structure
   
   PEVENT_PROFILING_STOP_CLEANUP_ARGS pStopProfiling = (PEVENT_PROFILING_STOP_CLEANUP_ARGS)malloc(sizeof (EVENT_PROFILING_STOP_CLEANUP_ARGS)) ;

   ZeroMemory(pStopProfiling, sizeof(PEVENT_PROFILING_STOP_CLEANUP_ARGS));

   // Populate the escape structure
   pStopProfiling->ulCmd = EVENT_PROFILING_ESC_STOP_CLEANUP_EVENT ;

   // Populate the escape structure
   pStopProfiling->bCleanUp = false;

   // call the escape wrapper function
   hr = DoEsc( (LPCSTR)pStopProfiling , sizeof (EVENT_PROFILING_STOP_CLEANUP_ARGS), NULL , 0);

   if(E_FAIL == hr)
   {
	   //just print the message . Continue processing as log can still be generated if the 
	   //event is not EVENT_OTHERS. For EVENT_OTHERS return.

	   printf("stop escape returned failure \n");

	   if(CUSTOM_EVENT == EventName)
	   {
		   free(pStopProfiling);
		   return hr;
	   }
   }

   //call create log
   lresult = CreateLog(LogFile);

   if (ERROR_SUCCESS != lresult )
   {
	   printf(" Log not created successfully");
	   hr = E_FAIL;
   }
		
  
   
   //add cleanup escape call

   PEVENT_PROFILING_STOP_CLEANUP_ARGS pCleanup = (PEVENT_PROFILING_STOP_CLEANUP_ARGS)malloc(sizeof (EVENT_PROFILING_STOP_CLEANUP_ARGS)) ;

   ZeroMemory(pCleanup, sizeof(EVENT_PROFILING_STOP_CLEANUP_ARGS));

   // Populate the escape structure
   pCleanup->ulCmd = EVENT_PROFILING_ESC_STOP_CLEANUP_EVENT ;

   pCleanup->bCleanUp = true;
   // call the escape wrapper function
   hr = DoEsc( (LPCSTR)pCleanup , sizeof (EVENT_PROFILING_STOP_CLEANUP_ARGS), NULL , 0);

   if(E_FAIL == hr)
   {
	   printf("stop escape returned failure \n");
   }

   free(pStopProfiling);
   free(pCleanup);
   return hr;
}

/***********************************************************************************

Function Name : IsEventProfilingComplete()

IN Paramters :

Purpose : Function to check event profiling completion. 
Return True if event profiling completed from driver side other wise return False.

Return Value: BOOLEAN - in case of success

************************************************************************************/
BOOLEAN IsEventProfilingComplete()
{
	HKEY hProfilingComplete;
	long lResult;
	DWORD dwReg_Value = 0;
	DWORD dwLpSize;
	DWORD dwLpType = REG_DWORD;
	ULONG size = sizeof(EVENT_PROFILING_INFO);
	PEVENT_PROFILING_INFO pEventProfileInfo;
	do
	{
		lResult = RegOpenKeyEx(
			HKEY_LOCAL_MACHINE,
			TEXT("SYSTEM\\CurrentControlSet\\services\\ialm\\Device0"),
			0,
			KEY_ALL_ACCESS,
			&hProfilingComplete
		);

		if (lResult != ERROR_SUCCESS)
		{
			if (lResult == ERROR_FILE_NOT_FOUND)
				printf("Key not found.\n");
			else
				printf("Error opening key.\n");
				return FALSE;
		}

		// Key successfully opened . Now query the value
		RegQueryValueEx(hProfilingComplete, TEXT("RegEventProfilingState"), 0, &dwLpType,
			(LPBYTE)&dwReg_Value, &dwLpSize);

		if (RegQueryValueEx(hProfilingComplete, TEXT("RegEventProfilingState"), 0, &dwLpType,
			(LPBYTE)&dwReg_Value, &dwLpSize) != ERROR_SUCCESS)
		{
			// Close Opened registry key.
			RegCloseKey(hProfilingComplete);
		}

	} while (PROFILING_STATE_COMPLETE != dwReg_Value);
	
	return (PROFILING_STATE_COMPLETE == dwReg_Value);
}

/***********************************************************************************

	Function Name : CreateLog ()

	IN Paramters : 

    Purpose : Function to collect the data which was written to the registry by the 
	          driver.The driver will write the address of the PEVENT_PROFILING_INFO 
			  into a windows registry key.The app will read that data and create the
			  log .

    Return Value: ERROR_SUCCESS - in case of success
	
************************************************************************************/

DWORD CreateLog(FILE* LogFile)
{
	// function to read the profiling data from registry.
	
	HKEY hProfilingComplete;
	long lResult;
    DWORD dwReg_Value;
	DWORD dwLpSize;
    DWORD dwLpType = REG_DWORD;
	ULONG size = sizeof(EVENT_PROFILING_INFO);	
	PEVENT_PROFILING_INFO pEventProfileInfo;
 
	// get binary data for complete profiling 
	lResult = RegOpenKeyEx(
							HKEY_LOCAL_MACHINE,
							TEXT("SYSTEM\\CurrentControlSet\\services\\ialm\\Device0"),
							0,
							KEY_ALL_ACCESS,
							&hProfilingComplete
							);  

	if (lResult != ERROR_SUCCESS) 
	{
		if (lResult == ERROR_FILE_NOT_FOUND) 
		{
			printf("Key not found.\n");
			return TRUE;
		} 
		else
		{
			printf("Error opening key.\n");
			return FALSE;
		}
	}

	dwLpType = REG_BINARY ;
	dwLpSize = size;
	pEventProfileInfo = (PEVENT_PROFILING_INFO)malloc(size);
	ZeroMemory(pEventProfileInfo, sizeof (EVENT_PROFILING_INFO));

	// Query for the complete value 
	lResult =  RegQueryValueEx(hProfilingComplete, TEXT("ProfilingToolValues"), 0,&dwLpType,(LPBYTE)pEventProfileInfo, &dwLpSize);

	// If the query call fails . It could be because of size mismatch.
	// reallocate memory with the size returned in the last query call
	// and query again
	
	if (lResult != ERROR_SUCCESS) 
	{
		ZeroMemory ( pEventProfileInfo, dwLpSize);
		lResult =  RegQueryValueEx(hProfilingComplete, TEXT("ProfilingToolValues"), 0,&dwLpType,(LPBYTE)pEventProfileInfo, &dwLpSize);
		if (lResult != ERROR_SUCCESS)
		{
			printf("\nRegistry Query call Failed\n");
			// Close Opened registry key.
			RegCloseKey(hProfilingComplete);
			free(pEventProfileInfo);
			return ERROR_QUERY_FAILED;
		}
	}

	// call the function to write the data into the log file .
	lResult = DumpData(pEventProfileInfo,LogFile);

	free(pEventProfileInfo);
	if (0 != lResult)
	{
		printf("DumpData failed \n");
		return ERROR ;
	}
	return ERROR_SUCCESS;
}

/***********************************************************************************

	Function Name : DumpData (PEVENT_PROFILING_INFO pEventProfileInfo)

	IN Paramters : pEventProfileInfo

    Purpose : Function will create the logs. It creates 2 files

			  1. Perf_Log_Tool.txt 
			  2. Perf_Log.Dat
              
			  The Text file is a mini log which will contain the Event name and the 
			  complete time takes.

			  The .DAT file will have the encrypted data . This file will be used by
			  the parser in order to create the detailed log file.

  Return Value : 0 - In case of success
                 1 - In case of Error

************************************************************************************/
int  DumpData(PEVENT_PROFILING_INFO pEventProfileInfo, FILE* LogFile)
{
   int i = 0 ;
   TCHAR  infoBuf[10];
   DWORD  bufCharCount = MAX_COMPUTERNAME_LENGTH+1;
   DWORD dwStatus=ERROR_SUCCESS;
   FILE* Fp = NULL ;
   const char*  OperatingSystem = "Windows" ;
   const char*  DxVersion = NULL ;
   // Get and display the name of the computer. 
   bufCharCount = INFO_BUFFER_SIZE;
   MEMORYSTATUSEX statex;
   OSVERSIONINFO osvi;
   SYSTEM_INFO siSysInfo;
   size_t datalength = 0 ;
   char* pTemp = NULL;
   char FileName[100];
   // Copy the hardware information to the SYSTEM_INFO structure. 
 
   GetSystemInfo(&siSysInfo); 

   // Get the OS version Info
   ZeroMemory(&osvi, sizeof(OSVERSIONINFO));
   osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);
   GetVersionEx(&osvi);
   if ((  6 == osvi.dwMajorVersion) &&(  1 == osvi.dwMinorVersion  ) )
   {
	  OperatingSystem = "Windows 7" ;
   }
   else if (( 6 == osvi.dwMajorVersion) &&( 2 == osvi.dwMinorVersion  ) )
   {
	  OperatingSystem = "Windows 8+" ;
   }
   statex.dwLength = sizeof (statex);
   GlobalMemoryStatusEx (&statex);

   // Get the computer name

   if(!GetComputerName( infoBuf,&bufCharCount))
	  printf("Error In getting Machine Name");
   
   // Check for user provided File Pointer
   if( NULL != LogFile)
   {
	   printf(" Creating Log file using App provided File Pointer\n");
	   Fp = LogFile;
   }
   else
   {
		printf(" Creating Log Files in default location\n ");
		//FileName = (char*)malloc(sizeof("GfxPerf")+sizeof(GetEventName(pEventProfileInfo->eEvent))+sizeof(".txt"));
		strcpy(FileName,"GfxPerf_");
		strcat(FileName,GetEventName(pEventProfileInfo->eEvent));
		strcat(FileName,".txt");
		// Open and write the TotalTime Taken into the text file
		 Fp = fopen( FileName ,"w");
   }

   //Remove Multiple power On and Off call
   LONGLONG llTotalExecTimeOfEventsWoMltplOnOff = 0; // Total Event execution time without multiple power on off call
   LONGLONG llPowerOnExecTime = 0; // it cant be -VE but its a LONGLONG param as,KeQueryPerformanceCounter returns in LONGLONG
   LONGLONG llPowerOffExecTime = 0; // it cant be -VE but its a LONGLONG param as,KeQueryPerformanceCounter returns in LONGLONG

   llTotalExecTimeOfEventsWoMltplOnOff = pEventProfileInfo->llTotalExecTimeOfEvent;
   for (UINT eventIndex = 0; eventIndex < MAX_STACK_SIZE_OF_CAPTURE; eventIndex++)
   {
	   if (pEventProfileInfo->stSequenceInfo[eventIndex].eDDIIndex == DDI_SETPOWER_ADP_ON_PROFILING_INDEX)
	   {
		   //For all multiple adapter on calls subtracting from total time.
		   llTotalExecTimeOfEventsWoMltplOnOff -= pEventProfileInfo->stSequenceInfo[eventIndex].llExecTime;
		   //Storing last adapter on DDI time.
		   llPowerOnExecTime = pEventProfileInfo->stSequenceInfo[eventIndex].llExecTime;
	   }
	   if (pEventProfileInfo->stSequenceInfo[eventIndex].eDDIIndex == DDI_SETPOWER_ADP_OFF_PROFILING_INDEX)
	   {
		   //For all multiple adapter off calls subtracting from total time.
		   llTotalExecTimeOfEventsWoMltplOnOff -= pEventProfileInfo->stSequenceInfo[eventIndex].llExecTime;
		   //Storing last adapter off DDI time.
		   llPowerOffExecTime = pEventProfileInfo->stSequenceInfo[eventIndex].llExecTime;
	   }
   }
   if (pEventProfileInfo->eEvent == EVENT_RESUME_FROM_SLEEP ||
	   pEventProfileInfo->eEvent == EVENT_RESUME_FROM_HIBERNATION ||
	   pEventProfileInfo->eEvent == EVENT_MONITOR_TURN_ON)
   {
	   //Adding last adapter on DDI time to total event time.
	   llTotalExecTimeOfEventsWoMltplOnOff += llPowerOnExecTime;
   }
   if (pEventProfileInfo->eEvent == EVENT_ENTER_SLEEP ||
	   pEventProfileInfo->eEvent == EVENT_ENTER_HIBERNATION ||
	   pEventProfileInfo->eEvent == EVENT_MONITOR_TURN_OFF)
   {
	   //Adding last adapter off DDI time to total event time.
	   llTotalExecTimeOfEventsWoMltplOnOff += llPowerOffExecTime;
   }
   
	fprintf(Fp ,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
	fprintf(Fp ," \t Performance Measurement Tool \n");
	fprintf(Fp ,"Operating System: %s %d\n",OperatingSystem,osvi.dwBuildNumber);
	fprintf(Fp ,"# of Processors: %u\n",siSysInfo.dwNumberOfProcessors);
	fprintf(Fp ,"Machine Name: %s",infoBuf);	 fprintf(Fp, "\n\n");

	fprintf(Fp ,"----------------------------------------------------------------------------------------------------------\n");
    fprintf(Fp , "////////////////////// MEMORY ////////////////////////////\n");
	fprintf(Fp , "Physical Memory : %d KB   ",statex.ullTotalPhys/DIV);
	fprintf(Fp ,  "Available Physical Memory : %d KB \n",statex.ullAvailPhys/DIV );
	fprintf(Fp , "Paging Memory :   %d KB   ", statex.ullTotalPageFile/DIV);
	fprintf(Fp , "Available Paging Memory : %d KB\n",statex.ullAvailPageFile/DIV );
	fprintf(Fp , "Virtual Memory:   %d KB   ",statex.ullTotalVirtual/DIV);
	fprintf(Fp,  "Available Virtual Memory :%d KB \n", statex.ullAvailVirtual/DIV );
	fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	fprintf(Fp , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
	fprintf(Fp, "\n\n");
	fprintf(Fp , "EventName: %s \n", GetEventName(pEventProfileInfo->eEvent));
	fprintf(Fp, "\n");
	fprintf(Fp , "Graphics Driver Time Taken for executing the Event :  %u microSeconds\n",pEventProfileInfo->llTotalExecTimeOfEvent);
	if (llTotalExecTimeOfEventsWoMltplOnOff != pEventProfileInfo->llTotalExecTimeOfEvent)
		fprintf(Fp, "Graphics Driver Time Taken for executing the Event without multiple on off call :  %u microSeconds\n", llTotalExecTimeOfEventsWoMltplOnOff);
	fprintf(Fp, "\n");
 	
	fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	fprintf(Fp , "END OF LOG  \n");
	fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");

    fprintf(Fp , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");

	fclose(Fp);

	printf("Log Created\n");
	//Create the .Dat file
	// junk values have been written to increase the size of the log 
	// parser knows where to read the good values from
	//FileName = (char*)malloc(sizeof("GfxPerf")+sizeof(GetEventName(pEventProfileInfo->eEvent))+sizeof(".txt"));
	strcpy(FileName,"GfxPerf");
	strcat(FileName,GetEventName(pEventProfileInfo->eEvent));
	strcat(FileName,".dat");
	Fp = fopen(FileName,"wb");
	
	// Write header of junk values

	for ( i = 0 ; i <= 100 ; i++ )
	{
		char junk = rand();
		fwrite( &junk,sizeof(char),1,Fp);
	}

	// Write the good data in encrypted format

	pTemp=(char*)pEventProfileInfo ;
	for ( i = 0 ; i < sizeof(EVENT_PROFILING_INFO); i++)
	{
		*pTemp = (*pTemp+ i);
		fwrite( pTemp,sizeof(char),1,Fp);
		pTemp++;
	}

	// Write the footer of junk values 
	for ( i = 0 ; i <= 100 ; i++ )
	{
		char junk = rand();
		fwrite( &junk,sizeof(char),1,Fp);
	}
	fclose(Fp);
	printf(" DAT FILE Created\n");
	return 0;
}

/***********************************************************************************

	Function Name : checksum ()

	IN Paramters : iSize - size of structure
				   pData - pointer to the structure
 
    OUT Parameters: checksum value

    Purpose : Function will get the checksum value to be assigned to the escape 
	          structure

************************************************************************************/
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
 
/***********************************************************************************

	Function Name : DoEsc ()

	IN Paramters : inData - size of structure
				   InSize - pointer to the structure being passed to the driver

    OUT Parameters: outData - pointer to the structure returned by the driver
                    OutSize - size of the out structure
 
    Purpose : Function is a wrapper for the D3DKMTEscape call
			  First it creates the escape structure and then calls the D3DKMTEscape()
			  function.

    Return Value: E_FAIL - Incase of Error
	              
				  S_OK -   Incase of Success

************************************************************************************/
HRESULT DoEsc(LPCSTR inData, int InSize , LPSTR outData, int OutSize )
{
   HRESULT hr = E_FAIL;
   HDC hDC = NULL;
   ULONG ulRet = -1;
   D3DKMT_OPENADAPTERFROMHDC* pOpenADapter = NULL;
   GFX_ESCAPE_HEADER_T *pHeader = NULL;
   D3DKMT_ESCAPE esc = {0};

   // Get the function pointers
   hGdi32 = LoadLibraryA("gdi32.dll");
   OpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32,"D3DKMTOpenAdapterFromHdc");
   D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32,"D3DKMTEscape");
   CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32,"D3DKMTCloseAdapter");
 
   //1. Getting Handle to Device Context
   DISPLAY_DEVICE dispDev;
   UINT devId = 0;
   ZeroMemory( &dispDev, sizeof(dispDev) );
   dispDev.cb = sizeof(dispDev);
   
   while (EnumDisplayDevices(NULL, devId++, &dispDev, 0))
   {
	   hDC = CreateDC(dispDev.DeviceName, NULL, NULL, 0);
	   /* Check if Device context is valid not*/
	   if (0 != hDC)
		   break;
   }
   if(hDC==NULL)
   {
       printf("\n\t\tHandle to DC not created !!");
	   hr=E_UNEXPECTED;
	   return hr;
   }

   SetLastError(0); 	//Setting Success till now

   //2. Open Adapter
   pOpenADapter = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
   ZeroMemory(pOpenADapter,sizeof(pOpenADapter));
   pOpenADapter->hDc = hDC;
   OpenAdapter(pOpenADapter);

   //3.Prepare Header
   pHeader = (GFX_ESCAPE_HEADER_T *)malloc(sizeof(GFX_ESCAPE_HEADER_T));
   if(NULL == pHeader)
   {
      hr = E_OUTOFMEMORY;
      //break;
   }

   ZeroMemory((void *)(pHeader),sizeof(GFX_ESCAPE_HEADER_T));
   pHeader->EscapeCode =  GFX_ESCAPE_EVENT_PROFILING; 
   pHeader->Size = InSize ;
   //Calculation of checksum value of buffer data for the header
   //(*pHeader)->CheckSum = checksumLocal(iDataSize,(PVOID)(pUserData));
   //TODO: Add checksum
   // pHeader->CheckSum = checksum(InSize,(void*)inData) ;
   pHeader->CheckSum =0 ;

   //4. Prepare Escape Structure

   esc.hAdapter = pOpenADapter->hAdapter;
   esc.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
   esc.pPrivateDriverData = (void*)malloc(InSize+sizeof(GFX_ESCAPE_HEADER_T));
   esc.PrivateDriverDataSize = InSize+sizeof(GFX_ESCAPE_HEADER_T);

   ZeroMemory((void *)(esc.pPrivateDriverData),InSize+sizeof(GFX_ESCAPE_HEADER_T));
   memcpy(esc.pPrivateDriverData,pHeader,sizeof(GFX_ESCAPE_HEADER_T));
   memcpy(((char*)esc.pPrivateDriverData+sizeof(GFX_ESCAPE_HEADER_T)),inData,InSize);

   //5. Call Escape Interface

    ulRet = D3DKmtEscape(&esc);
        
   //close adapter.
   D3DKMT_CLOSEADAPTER ca;
   ca.hAdapter = pOpenADapter->hAdapter;
   CloseAdapter(&ca);
   DeleteDC(hDC);

   //free all the mallocs

   if (pHeader != NULL )
   {
	   free(pHeader);
	   pHeader = NULL;
   }

   if (pOpenADapter != NULL)
   {
	   free(pOpenADapter);
	   pOpenADapter = NULL;
   }

   if (esc.pPrivateDriverData != NULL)
   {
	   free(esc.pPrivateDriverData);
	   esc.pPrivateDriverData = NULL;
   }
				
   if(ulRet == 0)
   {
      hr = S_OK;
   }
   else
   {
   
    LPVOID lpMsgBuf;
    LPVOID lpDisplayBuf;
	LPTSTR lpszFunction = NULL;
    DWORD dw = GetLastError(); 

    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | 
        FORMAT_MESSAGE_FROM_SYSTEM |
        FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,
        dw,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR) &lpMsgBuf,
        0, NULL );

    // Display the error message and exit the process

    lpDisplayBuf = (LPVOID)LocalAlloc(LMEM_ZEROINIT, 
        (lstrlen((LPCTSTR)lpMsgBuf) + lstrlen((LPCTSTR)lpszFunction) + 40) * sizeof(TCHAR)); 
    StringCchPrintf((LPTSTR)lpDisplayBuf, 
        LocalSize(lpDisplayBuf) / sizeof(TCHAR),
        TEXT("%s failed with error %d: %s"), 
        lpszFunction, dw, lpMsgBuf); 
    MessageBox(NULL, (LPCTSTR)lpDisplayBuf, TEXT("Error"), MB_OK); 

    LocalFree(lpMsgBuf);
    LocalFree(lpDisplayBuf);
   // ExitProcess(dw); 
   }
  return hr ;
}

/***********************************************************************************

	Function Name : GetEventName(int Event )

	IN Paramters : Event
 
    OUT Parameters: Char Pointer containing the Event Name

    Purpose : Function will get the Event Name  to be printed in the log

************************************************************************************/
char* GetEventName(int Event )
{

	switch (Event)
	{
		case  EVENT_ENTER_SLEEP:
			return "Event_Enter_Sleep";
		case  EVENT_RESUME_FROM_SLEEP:
			return "Event_Resume_From_Sleep";
		case  EVENT_ENTER_HIBERNATION:
			return "Event_Enter_Hibernation";
		case  EVENT_RESUME_FROM_HIBERNATION:
			return "Event_Resume_From_Hibernation";
		case  EVENT_MONITOR_TURN_OFF:
			return "Event_Monitor_Turn_Off";
		case  EVENT_MONITOR_TURN_ON:
			return "Event_Monitor_Turn_On";
		case  EVENT_MODE_CHANGE:
			return "Event_Mode_Change";
		case  EVENT_BOOT:
			return "Event_Boot";
		/*case  EVENT_SHUTDOWN:
			return "Event_Shutdown";*/
		case  CUSTOM_EVENT:
			return "Custom_Event";
		default:
			{
				return "WRONG_EVENT_VALUE";
			}
	}

}