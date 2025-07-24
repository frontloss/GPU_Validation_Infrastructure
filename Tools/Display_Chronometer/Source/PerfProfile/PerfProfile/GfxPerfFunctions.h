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
** File Name: GfxPerfFunctions.h
**
** Description: Functions exposed by the PerfProfile.dll
**
** Author : Shreyansh Sinha ( 4/10/2012 )
**
*******************************************************************************/


#ifndef _GFX_PERF_FUNC
#define _GFX_PERF_FUNC
#include <stdio.h>
// EXPOSED FUNCTIONS 
extern "C" 
{
	 
	  // Function to signal the driver to start profiling
	__declspec(dllexport) HRESULT __cdecl GfxStartProfiling(EVENT_NAME_PROFILING eEventName, bool bUseAppDependencyData , PDEPENDENCY_DDI_PROFILING pDependencyData  ); 
	  // Function to signal the end of profiling and creation of logs
    __declspec(dllexport) HRESULT __cdecl GfxStopProfiling(EVENT_NAME_PROFILING eEventName , FILE* fpLogFile ); 
}

#endif