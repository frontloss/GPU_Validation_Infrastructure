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
** File Name: PerfProfile.h
**
** Description: Contains functions declarations and Macros used by the 
				PerfProfile.dll
**
** Author : Shreyansh Sinha ( 4/10/2012 )
**
*******************************************************************************/
#ifndef _PERF_PROFILE_

#define _PERF_PROFILE_
#include  <stdio.h>
#include  "stdafx.h"
#include  "windows.h"
#ifndef NTSTATUS
#define NTSTATUS int
#endif
#include <d3dkmthk.h>
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// ERROR for registry query failure
#define				   ERROR_QUERY_FAILED 13

// values for system memory calculations
#define				   INFO_BUFFER_SIZE 32767
#define			       DIV              1024

// Version Number of the DLL
#define PROFILING_VERSION_NUMBER          1


// Internal Functions used by the DLL

HRESULT DoEsc(LPCSTR inData, int InSize , LPSTR outData, int OutSize );
DWORD CreateLog(FILE* LogFile);
char* GetEventName(int Event);
BOOLEAN IsEventProfilingComplete();
 // First function to be called by the APP for version checking
 HRESULT  GfxInitProfiling( ULONG ulVersionNumber); 
#endif 