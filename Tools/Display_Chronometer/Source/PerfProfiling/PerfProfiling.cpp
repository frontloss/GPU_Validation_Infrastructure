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
** File Name: PerfProfiling.cpp
**
** Description: Contains functions definitions used in the PerfProfiling tool
**
** Author : Shreyansh Sinha ( 4/10/2012 )
**
*******************************************************************************/
#include <stdio.h>
#include "stdafx.h"
#include <Windows.h>
#include <GfxPerfEvents.h>
#include <GfxPerfFunctions.h>
#include <powrprof.h>

// FORWARD DECLARTIONS 
typedef HRESULT ( __cdecl *ProcAdd)(EVENT_NAME_PROFILING , bool , PDEPENDENCY_DDI_PROFILING);
typedef HRESULT ( __cdecl *InitAdd)(ULONG );
typedef DWORD ( __cdecl *Logger)();
typedef HRESULT ( __cdecl *StopAdd)(EVENT_NAME_PROFILING , FILE* );

boolean CheckForBootEvent(int*Event);


/***********************************************************************************

	Function Name : TimerAPCProc ()

	IN Paramters : 

	Purpose : This is the callback for the Timer set to resume the system from S3 or S4

***********************************************************************************/
VOID CALLBACK TimerAPCProc(
  __in_opt  LPVOID lpArgToCompletionRoutine,
  __in      DWORD dwTimerLowValue,
  __in      DWORD dwTimerHighValue
)
{
	SetThreadExecutionState(ES_CONTINUOUS|ES_DISPLAY_REQUIRED|ES_SYSTEM_REQUIRED);
	//printf(" inside APC ");

}

/***********************************************************************************

	Function Name : Main ()

	IN Paramters : argc - Number of arguments
	               argv - List of arguments

    Purpose : Entry function of the command line tool 

************************************************************************************/
int _tmain(int argc, _TCHAR* argv[])
{
	int Event = 0 ;
	HRESULT hr = E_FAIL ;
	HMODULE hPerf = NULL ;
	InitAdd Initialize = NULL ;
	ProcAdd StartTiming = NULL ;
	Logger  CreateLog = NULL;
    SYSTEM_POWER_CAPABILITIES stSystemPowerCapabilities ;

    BOOLEAN bReturn = GetPwrCapabilities( &stSystemPowerCapabilities );
	//getchar();
	
	// Load the PerfProfile DLL 

	hPerf   = LoadLibraryA("PerfProfile.dll");

	if(NULL == hPerf)
	{
		printf("PerfProfile.dll could not be loaded\n");
		printf("Check if PerfProfile.dll is present\n");
		return hr;
	}

	// If number of command line arguments is 1 it means that the tool has been run without parameters.
	// Check if its after a boot event profiling . Otherwise exit 
	if ( argc == 1 ) 
	{
 	
		if (CheckForBootEvent(&Event))
		{
			// the tool has been run without parameters and after boot event profiling has been
			// done . So call GfxStopProfiling() to create log and cleanup 

			StopAdd Stop = (StopAdd) GetProcAddress(hPerf,"GfxStopProfiling") ;
	
			if(NULL != Stop)
			{
				(Stop)((EVENT_NAME_PROFILING)Event,NULL);
			}
		}
	}

	else if ( argc > 1)
	{
      // Tool has been run with Paramters , check if user wants HELP menu 
     if ( (!wcscmp( TEXT("help"),argv[1]))||(!wcscmp( TEXT("/?"),argv[1])))
	 {
		printf ( " PerfProfiling Version 1.0 \n\n ");
		printf ( " Syntax : \n ");
		printf ( " PerfProfiling.exe [ Event Name] \n\n");
		printf ( " List of Events/Options :\n\n");
		printf ( " EVENT_ENTER_SLEEP : 1\n ");
		printf ( " EVENT_RESUME_FROM_SLEEP : 2\n ");
		printf ( " EVENT_ENTER_HIBERNATION : 3\n ");
		printf ( " EVENT_RESUME_FROM_HIBERNATION : 4\n ");
		printf ( " EVENT_MONITOR_TURN_OFF : 5\n ");
		printf ( " EVENT_MONITOR_TURN_ON : 6\n ");
		printf ( " EVENT_MODE_CHANGE : 7\n ");
		printf ( " EVENT_BOOT : 8\n ");
		printf ( " CUSTOM_EVENT: 9\n ");
		printf ("\n");
		printf ( " Example: To Profile Time for Entering Sleep\n");
		printf ( " PerfProfiling.exe 1 \n\n");
		printf ( " Example: For Help\n");
		printf ( " PerfProfiling.exe help \n");
		printf ( "For more details please refer to Performance Profiling Tool.docx\n");
		return 1 ;
	 }   

    // User has entered a valid EVENT 

    Event = _wtoi(argv[1]);

	// Call the Init function . It should pass the versioning info

	Initialize = (InitAdd) GetProcAddress(hPerf, "GfxInitProfiling");
	if ( NULL != Initialize)
	{
		hr = (Initialize)(1);
		if (S_OK != hr )
		  return 1;
    }

	// Send the START escape in order to notify the driver to get ready to start profiling

	StartTiming = (ProcAdd) GetProcAddress(hPerf, "GfxStartProfiling"); 

	// For Monitor_on event we will send the escape just before triggering the Monitor On event
    if ( (0 != bReturn) && (TRUE == stSystemPowerCapabilities.AoAc) )
    {
	        if ((NULL != StartTiming)) 
            { 
		          hr =  (StartTiming) ((EVENT_NAME_PROFILING)Event,false,NULL); 
		          if (S_OK != hr )
		          return 1;
            }
    }
    else
    {
        	if ((NULL != StartTiming)&&(EVENT_MONITOR_TURN_ON != Event  )) 
            { 
		        hr =  (StartTiming) ((EVENT_NAME_PROFILING)Event,false,NULL); 
		        if (S_OK != hr )
		        return 1;
            }
    }
	//trigger the event requested by the user

	switch( Event )
	{
		case EVENT_ENTER_SLEEP:
		/*{
			SetSuspendState( false , true ,false);
			break;
		}*/
		
		case EVENT_RESUME_FROM_SLEEP:	  
		{

            if ( (0 != bReturn) && (TRUE == stSystemPowerCapabilities.AoAc) )
            {
                //MessageBox( NULL,TEXT("aoac supported"),TEXT ("aoac"),MB_OK);
                const int MONITOR_ON = -1;
			    const int MONITOR_OFF = 2;
			    const int MONITOR_STANBY = 1;
			
			    PostMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF);
  			    break ;
            }
            else
            {
                HANDLE hTimer = NULL;
			    LARGE_INTEGER liDueTime;
			    SYSTEMTIME LocalTime;
			    FILETIME ftTemp;
			    FILETIME ftUTC;
			
			    // 5 seconds delay 
			
			    /*LARGE_INTEGER WakeTime;

			    WakeTime.QuadPart = (10 * 10000000);
			    liDueTime.QuadPart = - WakeTime.QuadPart;*/

			    GetLocalTime( &LocalTime);

			    LocalTime.wSecond = LocalTime.wSecond + 20;

			    SystemTimeToFileTime( &LocalTime,&ftTemp);

			    LocalFileTimeToFileTime( &ftTemp,&ftUTC);

			    liDueTime.LowPart = ftUTC.dwLowDateTime;

			    liDueTime.HighPart = ftUTC.dwHighDateTime;


			    // Create an unnamed waitable timer.
			    hTimer = CreateWaitableTimer(NULL, TRUE, NULL);
			    if (NULL == hTimer)
			    {
				    printf("CreateWaitableTimer failed (%d)\n", GetLastError());
				    return 1;
			    }

			    if (!SetWaitableTimer(hTimer, &liDueTime, 0, TimerAPCProc, NULL, true))
			    {
				    printf("SetWaitableTimer failed (%d)\n", GetLastError());
				    return 2;
			    }
			    printf("SetWaitableTimer(%d)\n", GetLastError());
			    // Wait for the timer.
			    SetSuspendState( false , true ,false);
			
			    if (WaitForSingleObjectEx(hTimer, INFINITE, TRUE) != WAIT_OBJECT_0)
			    {
				    //printf("WaitForSingleObject failed (%d)\n", GetLastError());
			    }
			    else printf("Timer was signaled.\n");
			
			    break;
            }

            break;
		}

		case EVENT_ENTER_HIBERNATION:
		/*{
			SetSuspendState( true , true ,false);
			break;
		}*/
		case EVENT_RESUME_FROM_HIBERNATION:
		{
			HANDLE hTimer = NULL;
			LARGE_INTEGER liDueTime;
			SYSTEMTIME LocalTime;
			FILETIME ftTemp;
			FILETIME ftUTC;
			// 10 seconds delay .In Nano seconds
			/*LARGE_INTEGER WakeTime;

			WakeTime.QuadPart = (10 * 10000000);
			liDueTime.QuadPart = - WakeTime.QuadPart;*/

			GetLocalTime( &LocalTime);

			LocalTime.wSecond = LocalTime.wSecond + 20;

			SystemTimeToFileTime( &LocalTime,&ftTemp);

			LocalFileTimeToFileTime( &ftTemp,&ftUTC);

			liDueTime.LowPart = ftUTC.dwLowDateTime;

			liDueTime.HighPart = ftUTC.dwHighDateTime;


			// Create an unnamed waitable timer.
			hTimer = CreateWaitableTimer(NULL, TRUE, NULL);
			if (NULL == hTimer)
			{
				printf("CreateWaitableTimer failed (%d)\n", GetLastError());
				return 1;
			}

			if (!SetWaitableTimer(hTimer, &liDueTime, 0, TimerAPCProc, NULL, true))
			{
				printf("SetWaitableTimer failed (%d)\n", GetLastError());
				return 2;
			}
			printf("SetWaitableTimer(%d)\n", GetLastError());
			// Wait for the timer.
			SetSuspendState( true , true ,false);
			
			if (WaitForSingleObjectEx(hTimer, INFINITE, TRUE) != WAIT_OBJECT_0)
			{
				//printf("WaitForSingleObject failed (%d)\n", GetLastError());
			}
			else printf("Timer was signaled.\n");
			
			break;
			
			break;
		}
		case EVENT_MONITOR_TURN_OFF:
		/*{
			const int MONITOR_ON = -1;
			const int MONITOR_OFF = 2;
			const int MONITOR_STANBY = 1;
			
			SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF);
 			break ;
		}*/
		case EVENT_MONITOR_TURN_ON:
		{
            const int MONITOR_ON = -1;
			const int MONITOR_OFF = 2;
			const int MONITOR_STANBY = 1;
			
			PostMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF);

            if ( (0 != bReturn) && (FALSE == stSystemPowerCapabilities.AoAc) )
            {
	  		
  			    ::Sleep( 5000);

			    // send the start escape to driver before turning on the monitor
 			     hr =  (StartTiming) ((EVENT_NAME_PROFILING)Event,false,NULL); 

			     if (S_OK != hr )
				     return 1;

                // Turn on the monitor
 			    PostMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_ON);
            }
			break ;
		}
		case EVENT_MODE_CHANGE:
		{
			UINT32 pNumPathArrayElements = 0 ;
			DISPLAYCONFIG_PATH_INFO *pPathInfoArray  ;
			UINT32 pNumModeInfoArrayElements = 0 ;
			DISPLAYCONFIG_MODE_INFO *pModeInfoArray;
			LONG lReturn = 0;

			// Get the buffer sizes
			lReturn = GetDisplayConfigBufferSizes(QDC_ALL_PATHS,&pNumPathArrayElements, &pNumModeInfoArrayElements);
			if( ERROR_SUCCESS == lReturn)
			{
				pPathInfoArray = (DISPLAYCONFIG_PATH_INFO*)malloc((pNumPathArrayElements) * sizeof(DISPLAYCONFIG_PATH_INFO));
				memset(pPathInfoArray, 0, (pNumPathArrayElements) * sizeof(DISPLAYCONFIG_PATH_INFO));

				pModeInfoArray = (DISPLAYCONFIG_MODE_INFO*)malloc((pNumModeInfoArrayElements) * sizeof(DISPLAYCONFIG_MODE_INFO));
				memset(pModeInfoArray, 0, (pNumModeInfoArrayElements) * sizeof(DISPLAYCONFIG_MODE_INFO));

               // Call QDC to get the PathInfo
			   lReturn = QueryDisplayConfig(QDC_ALL_PATHS,&pNumPathArrayElements,pPathInfoArray,&pNumModeInfoArrayElements,pModeInfoArray,NULL);

			   if( ERROR_SUCCESS == lReturn)
			   {
				   // Setting the SDC Flags
					DWORD sdcOptions = 0;

					// Always set the below flags
					sdcOptions = SDC_APPLY|SDC_USE_SUPPLIED_DISPLAY_CONFIG|SDC_SAVE_TO_DATABASE|SDC_NO_OPTIMIZATION;

					// querying the current mode using the QDC call and then setting the same resolution again
					// Since the NO_OPTIMIZATION flag is set the SDC call successfully applies the same resolution
					// again
					lReturn = SetDisplayConfig( pNumPathArrayElements,pPathInfoArray,pNumModeInfoArrayElements,pModeInfoArray,sdcOptions);

					if( ERROR_SUCCESS != lReturn)
					{
						printf("Set Mode Failed");
					}
			   }
			}
			free(pPathInfoArray);
			free(pModeInfoArray);

		    break;
		}
		case EVENT_BOOT:
		{
			HANDLE hToken; 
			TOKEN_PRIVILEGES tkp; 
 
			// Get a token for this process. 
 
			if (!OpenProcessToken(GetCurrentProcess(), 
			 TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) 
			 return( FALSE ); 
 
			// Get the LUID for the shutdown privilege. 
 
			LookupPrivilegeValue(NULL, SE_SHUTDOWN_NAME, 
				&tkp.Privileges[0].Luid); 
 
			tkp.PrivilegeCount = 1;  // one privilege to set    
			tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED; 
 
			// Get the shutdown privilege for this process. 
 
			AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, 
			 (PTOKEN_PRIVILEGES)NULL, 0); 
 
			if (GetLastError() != ERROR_SUCCESS) 
			 return FALSE; 

			ExitWindowsEx(EWX_REBOOT|EWX_FORCE,  SHTDN_REASON_MAJOR_OPERATINGSYSTEM|SHTDN_REASON_MINOR_UPGRADE|SHTDN_REASON_FLAG_PLANNED) ;

			break ;
		}
		//case EVENT_SHUTDOWN:
		//{
		//	HANDLE hToken; 
		//	TOKEN_PRIVILEGES tkp; 
 
		//	// Get a token for this process. 
 
		//	if (!OpenProcessToken(GetCurrentProcess(), 
		//	 TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) 
		//	 return( FALSE ); 
 
		//	// Get the LUID for the shutdown privilege. 
 
		//	LookupPrivilegeValue(NULL, SE_SHUTDOWN_NAME, 
		//		&tkp.Privileges[0].Luid); 
 
		//	tkp.PrivilegeCount = 1;  // one privilege to set    
		//	tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED; 
 
		//	// Get the shutdown privilege for this process. 
 
		//	AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, 
		//	 (PTOKEN_PRIVILEGES)NULL, 0); 
 
		//	if (GetLastError() != ERROR_SUCCESS) 
		//	 return FALSE; 

		//	ExitWindowsEx(EWX_SHUTDOWN | EWX_FORCE,  SHTDN_REASON_MAJOR_OPERATINGSYSTEM|SHTDN_REASON_MINOR_UPGRADE|SHTDN_REASON_FLAG_PLANNED) ;

		//	break;
		//}
     case CUSTOM_EVENT:
		{
			char input ;
			printf(" Press 'Y' to stop profiling : \n");
			input = (char)getchar();

		    while(('Y'!= input) && ('y'!= input)) 
			{
				printf("Wrong Input, Continuing Profiling \n");
				printf(" Press 'Y' to stop profiling : \n");
				input = getchar();
			}
			
			break;
		}
	 default :
		{
			printf(" WRONG EVENT NAME \n");
			printf ( " PerfProfiling Version 1.0 \n\n ");
			printf ( " Syntax : \n ");
			printf ( " PerfProfiling.exe [ Event Name] \n\n");
			printf ( " List of Events/Options :\n\n");
			printf ( " EVENT_ENTER_SLEEP : 1\n ");
			printf ( " EVENT_RESUME_FROM_SLEEP : 2\n ");
			printf ( " EVENT_ENTER_HIBERNATION : 3\n ");
			printf ( " EVENT_RESUME_FROM_HIBERNATION : 4\n ");
			printf ( " EVENT_MONITOR_TURN_OFF : 5\n ");
			printf ( " EVENT_MONITOR_TURN_ON : 6\n ");
			printf ( " EVENT_MODE_CHANGE : 7\n ");
			printf ( " EVENT_BOOT : 8\n ");
			printf ( " CUSTOME_EVENT: 9\n ");
			printf ("\n");
			printf ( " Example: To Profile Time for Entering Sleep\n");
			printf ( " PerfProfiling.exe 1 \n\n");
			printf ( " Example: For Help\n");
			printf ( " PerfProfiling.exe help \n");
		
			return 1;
		}
	}

	// Send the STOP escape to the driver to clean up and create the logs . If its the Event to be profiled 
	// is ShutDown or Boot we dont send the stop escape as the profiling wouldn't be complete
	// at this point.
		
	//if ( ( EVENT_SHUTDOWN != Event ) && (EVENT_BOOT != Event ) )
	if ( EVENT_BOOT != Event  )
	{
		
		StopAdd Stop = (StopAdd) GetProcAddress(hPerf,"GfxStopProfiling") ;
	
		if(NULL != Stop)
		{
			(Stop)((EVENT_NAME_PROFILING)Event, NULL);
		}
	}
	
	}
	return 0;
}

/***********************************************************************************

	Function Name : CheckForBootEvent ()

	IN_OUT Paramters : Event 

    Purpose : This function checks for the Event stored in the Windows Registry if it's
	          a boot event i.e Shutdown or Restart it returns TRUE and the Event

************************************************************************************/
boolean CheckForBootEvent(int* Event)
{
	HKEY BaseKey ;
	long lResult;
    DWORD dwReg_Value ;
	DWORD dwLpSize;
    DWORD dwLpType = REG_DWORD;
	
	// Open the Device0 key 
	lResult = RegOpenKeyEx(
							HKEY_LOCAL_MACHINE,
							TEXT("SYSTEM\\CurrentControlSet\\services\\ialm\\Device0"),
							0,
							KEY_ALL_ACCESS,//KEY_READ|KEY_QUERY_VALUE,
							&BaseKey
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
    
	// Query the value of the ProfilingToolEvent key
	lResult = RegQueryValueEx(BaseKey, TEXT("ProfilingToolEvent"), 0,&dwLpType,
                       (LPBYTE)&dwReg_Value, &dwLpSize);

	if(RegQueryValueEx(BaseKey, TEXT("ProfilingToolEvent"), 0,&dwLpType,
                       (LPBYTE)&dwReg_Value, &dwLpSize)!=ERROR_SUCCESS)
	{
		// Close Opened registry key.
		printf("\nRegistry Query call Failed\n");
		RegCloseKey(BaseKey);		
		return false;
	}

	// check if it's a boot event 
	/*if( (EVENT_BOOT == dwReg_Value) || (EVENT_SHUTDOWN == dwReg_Value))*/
	if(EVENT_BOOT == dwReg_Value)
	{
		// its a boot event so return TRUE
		*Event = dwReg_Value;
		return true;
	}

	return false;
}