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
** File Name: PerfParser.cpp
**
** Description: Contains functions and Macros used by the PerfParser.exe
**
** Author : Shreyansh Sinha ( 4/10/2012 )
**
*******************************************************************************/

#include "stdafx.h"
#include "windows.h"
#include <malloc.h>
#include <Event_Profiling.h>
//#include "Event_Profiling.h"
#include "PerfParser.h"

/***********************************************************************************

	Function Name : Main ()

	IN Paramters : argc - Number of arguments
	               argv - List of arguments

    Purpose : Entry function of the command line Parser 

************************************************************************************/

int _tmain(int argc, _TCHAR* argv[])
{
	//getchar();
	int i = 0 ;
	char junk;
	PEVENT_PROFILING_INFO pEventProfileInfo = NULL ;
	FILE* Fp = NULL;
	HKEY  hProfilingVersion;
	DWORD dwReg_Value ;
	DWORD dwLpSize;
	DWORD dwLpType = REG_DWORD;
	long  lResult;
	void* pTemp = NULL;
	char* pCurrentPos = NULL;
	DWORD error = 0 ;

	lResult = RegOpenKeyEx(
								HKEY_LOCAL_MACHINE,
								TEXT("SYSTEM\\CurrentControlSet\\services\\ialm\\Device0"),
								0,
								KEY_ALL_ACCESS,
								&hProfilingVersion
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
    
		// Key successfully opened . Now query the value
		lResult = RegQueryValueEx(hProfilingVersion, TEXT("ProfilingToolVersion"), 0,&dwLpType,
                       (LPBYTE)&dwReg_Value, &dwLpSize);
		if(RegQueryValueEx(hProfilingVersion, TEXT("ProfilingToolVersion"), 0,&dwLpType,
                       (LPBYTE)&dwReg_Value, &dwLpSize)!=ERROR_SUCCESS)
		{
			printf("\nRegistry Query call Failed\n");

			// Close Opened registry key.
			RegCloseKey(hProfilingVersion);	

			return ERROR_QUERY_FAILED;
		}

	if ( PROFILING_VERSION_NUMBER != dwReg_Value)
	{
		printf("Version Mismatch\n PARSER Version is %d",PROFILING_VERSION_NUMBER);
		return ERROR;
	}
	size_t length = sizeof(EVENT_PROFILING_INFO);
	////// add version check
	// open the dat file
	Fp = _wfopen( argv[1] ,L"rb");

	error = GetLastError();

	if(NULL == Fp)
	{
		printf("Could Not Open .Dat file\n");
		printf(" GetLastError() returned error code %d ",error);
		return 1;
	}

	
	// reading the junk values in the header
	for ( i = 0 ; i<= 100 ; i++)
	{
		fread(&junk,sizeof(char),1,Fp);
	}

	pTemp = malloc(sizeof (EVENT_PROFILING_INFO));
	pCurrentPos = (char*)pTemp;
	
	//reading the good value
	for ( i = 0 ; i < sizeof(EVENT_PROFILING_INFO);i++)
	{
		fread(pCurrentPos, sizeof(char),1,Fp);
		*pCurrentPos = ( *pCurrentPos-i);
		pCurrentPos++;
	}
	
	// type cast the pTemp into PEventProfilingInfo
	pEventProfileInfo = (PEVENT_PROFILING_INFO)pTemp;

	printf("Parsing Done\n");

	// close the .dat file
	fclose(Fp);

	
	printf("Creating full log\n");
	// call the Dump function to create the full log 
	DumpData(pEventProfileInfo);
	free(pTemp);
	return 0;
}

/***********************************************************************************

	Function Name : DumpData ()

	IN Paramters : pEventProfileInfo - Pointer to the structure contaiing the full
									   data

    Purpose : Function will create the detailed log file "Perf_Log_Parser.txt"

************************************************************************************/
int  DumpData(PEVENT_PROFILING_INFO pEventProfileInfo)
{
  ULONG   counter ;
  char*  infoBuf;
  DWORD  bufCharCount = MAX_COMPUTERNAME_LENGTH+1;
  DWORD dwStatus=ERROR_SUCCESS;
  FILE* Fp = NULL ;
  const char*  OperatingSystem = "Windows" ;
  char FileName[50];
  // Get and display the name of the computer. 
  MEMORYSTATUSEX statex;
  OSVERSIONINFO osvi;
  SYSTEM_INFO siSysInfo;
  
  infoBuf = (char*)malloc(bufCharCount*sizeof(TCHAR));
   // Copy the hardware information to the SYSTEM_INFO structure. 
 
   GetSystemInfo(&siSysInfo); 

  
  ZeroMemory(&osvi, sizeof(OSVERSIONINFO));
  osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);
  GetVersionEx(&osvi);
  if ((6 == osvi.dwMajorVersion ) &&( 1 == osvi.dwMinorVersion  ) )
  {
	  OperatingSystem = "Windows 7" ;
  }
  else if ((6 == osvi.dwMajorVersion  ) &&(2 == osvi.dwMinorVersion  ) )
  {
	  OperatingSystem = "Windows 8+" ;
  }
  statex.dwLength = sizeof (statex);
  GlobalMemoryStatusEx (&statex);

  if(!GetComputerName( (LPWSTR)infoBuf,&bufCharCount))
	  printf("Error In getting Machine Name");

   // FileName = (char*)malloc(sizeof("GfxPerf")+sizeof(GetEventName(pEventProfileInfo->eEvent))+sizeof(".txt"));
	strcpy(FileName,"GfxPerf_");
	strcat(FileName,GetEventName(pEventProfileInfo->eEvent));
	strcat(FileName,"_Full.txt");

     Fp = fopen(FileName ,"w");
	 fprintf(Fp ,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
	 fprintf(Fp ," \t Performance Measurement Tool \n");
	 fprintf(Fp ,"Operating System: %s %d\n",OperatingSystem,osvi.dwBuildNumber);
	 fprintf(Fp ,"# of Processors: %u\n",siSysInfo.dwNumberOfProcessors);
	 fprintf(Fp ,"Machine Name: %s",infoBuf);	 fprintf(Fp, "\n\n");

	 fprintf(Fp ,"----------------------------------------------------------------------------------------------------------\n");
     fprintf(Fp , "////////////////////// MEMORY ////////////////////////////\n");
	 fprintf(Fp , "Physical Memory : %d KB   ",statex.ullTotalPhys/DIV);
	 fprintf(Fp,  "Available Physical Memory : %d KB \n",statex.ullAvailPhys/DIV );
	 fprintf(Fp , "Paging Memory :   %d KB   ", statex.ullTotalPageFile/DIV);
	 fprintf(Fp , "Available Paging Memory : %d KB\n",statex.ullAvailPageFile/DIV );
	 fprintf(Fp , "Virtual Memory:   %d KB   ",statex.ullTotalVirtual/DIV);
	 fprintf(Fp,  "Available Virtual Memory :%d KB \n", statex.ullAvailVirtual/DIV );
	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	 fprintf(Fp , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
	 fprintf(Fp, "\n\n");
	 fprintf(Fp , "EventName: %s \n", GetEventName(pEventProfileInfo->eEvent));
	 fprintf(Fp, "\n");
	 fprintf(Fp , "Graphics Driver Time Taken for executing the Event :  %u microSeconds\n",pEventProfileInfo->llTotalExecTimeOfEvent);
	 fprintf(Fp, "\n");
 	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");

	 fprintf(Fp , " \t \t \t \t \t DDI CALL SEQUENCE FOR THE EVENT:\n");
	 fprintf(Fp , " DDI NAME \t \t \t \t \t \t \t TIME TAKEN (in micro Seconds) \n");
	 fprintf(Fp , " _________________________________________________________________________________________________________\n\n");
	 for (counter = 0; counter < pEventProfileInfo->ulNumCallsInSequence; counter++  )
	 {
		  if( pEventProfileInfo->stSequenceInfo[counter].eDDIIndex > DDI_CONTROL_INTERRUPT_PROFILING_INDEX)
		 {
			 fprintf(Fp, "\t");
	 		 fprintf(Fp , " %-50s \t %u \n\n",(pEventProfileInfo->stProfilingInfo[pEventProfileInfo->stSequenceInfo[counter].eDDIIndex]).chFuncName , pEventProfileInfo->stSequenceInfo[counter].llExecTime);
		 }
		 else
		 {
		 fprintf(Fp , " %-50s \t \t %u \n\n",(pEventProfileInfo->stProfilingInfo[pEventProfileInfo->stSequenceInfo[counter].eDDIIndex]).chFuncName , pEventProfileInfo->stSequenceInfo[counter].llExecTime);
		 }
	 }

	
	
	 fprintf(Fp, "\n");

	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	 fprintf(Fp , "\t \t \t \t Per DDI Profiling Data for the Event  \n");
	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");

	 fprintf(Fp , "\n");

	 
	 fprintf(Fp , " DDI NAME \t \t \t \t \t No of Times Called \t Total DDI Execution Time \n");
	 fprintf(Fp , " __________________________________________________________________________________________________________\n\n");
	
	 fprintf(Fp , "\n");
	 for (counter = 0; counter < MAX_DDI_PROFILING_INDEX ; counter++  )
	 {
		 if(0 != pEventProfileInfo->stProfilingInfo[counter].ulNumTimesCalled)
		 {
			 fprintf(Fp , " %-50s \t \t %d \t %u \n ", pEventProfileInfo->stProfilingInfo[counter].chFuncName ,pEventProfileInfo->stProfilingInfo[counter].ulNumTimesCalled, pEventProfileInfo->stProfilingInfo[counter].llTotalDDIExecTime);

			 fprintf(Fp , "\n");
		 }
	 }
	 fprintf(Fp, "\n");

	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	 fprintf(Fp , "\t \t \t \t Bucketing log based on Execution times for each DDI \n");
	 fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");

	 fprintf(Fp , "\n");
	 fprintf(Fp , " DDI NAME \t \t \t \t \t \t \t  0-10 ms \t 10-50 ms \t >50 ms \n");
 	 fprintf(Fp , " __________________________________________________________________________________________________________\n\n\n");
	 for (counter = 0; counter < MAX_DDI_PROFILING_INDEX ; counter++  )
	 {
		 if(0 != pEventProfileInfo->stProfilingInfo[counter].ulNumTimesCalled)
		 {
			 fprintf(Fp , " %-50s \t \t  %d \t \t %d \t \t %d \n ", pEventProfileInfo->stProfilingInfo[counter].chFuncName ,pEventProfileInfo->stProfilingInfo[counter].ulNumCallsExecTimeInLowRange ,pEventProfileInfo->stProfilingInfo[counter].ulNumCallsExecTimeInHighRange ,pEventProfileInfo->stProfilingInfo[counter].ulNumCallsExecTimeInOutOfRange);

			 fprintf(Fp , "\n");
		 }
	 }
	 fprintf(Fp, "\n");

	fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");
	fprintf(Fp , "END OF LOG  \n");
	fprintf(Fp , "----------------------------------------------------------------------------------------------------------\n");

	fprintf(Fp , "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");

	fclose(Fp);
	printf("Full log created\n");

	free(infoBuf);
	return 0;
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