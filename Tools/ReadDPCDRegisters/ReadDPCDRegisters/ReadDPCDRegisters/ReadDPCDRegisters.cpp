// ReadDPCDRegisters.cpp : Defines the entry point for the console application.

#include "stdafx.h"

/* System Includes */
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

/* User Includes*/
#include "ReadDPCDRegisters.h"

#define BUFFER_SIZE 512

/* Strutures and variables to hold the fetched data*/
HMODULE hSysUtilLib = NULL;
HMODULE hDispConfLib = NULL;
HRESULT errorCode = S_OK;

/* Register to check escape and MMIO read interfaces*/
ULONG ulOffset = 0x70180;
ULONG value = 0;

/* Structures to test the DLL functionalities*/
ENUMERATED_DISPLAYS enuDisplay;

bool DPCDRead(ULONG ulStartOffset, UINT targetID, ULONG ulDpcdBuffer[], UINT dpcdBufferSize);

/* Main entry point*/
int main()
{
	int status = FALSE;

	do
	{
		/* Load and verify */
		hSysUtilLib = LoadSystemUtilityDLL();
		if (NULL == hSysUtilLib)
		{
			printf("\nFailed to Load SystemUtility DLL\n");
			break;
		}

		// Read DPCD registers now
		ReadDPCDRegisters();

		status = TRUE;

	} while (FALSE);

	return status;
}

/* Load systemutility DLL*/
HMODULE LoadSystemUtilityDLL()
{
	HMODULE retVal = NULL;

	/* Load DLLs and get the handle */
	retVal = LoadLibraryA("SystemUtility.dll");
	if (retVal == NULL)
	{
		printf("System utility DLL load failed with error code: %d\n", GetLastError());
		return retVal;
	}

	return retVal;
}

void ReadDPCDRegisters()
{
	UINT targetID = 0;
	ULONG offset = 0;
	ULONG dpcdBuffer[BUFFER_SIZE];

	enuDisplay.Size = sizeof(ENUMERATED_DISPLAYS);

	PFN_EDISPLAY_INFO_ADD pfnGetEnumDisplay = (PFN_EDISPLAY_INFO_ADD)GetProcAddress(hSysUtilLib, "GetEnumeratedDisplayInfo");
	(pfnGetEnumDisplay)(&enuDisplay, &errorCode);

	printf("\nTotal number of enumerated Displays: %d\n", enuDisplay.Count);

	if (errorCode != S_OK)
	{
		printf("\nCheckGetEnumeratedDisplayInfo() returned error code %d\n", errorCode);
		getchar();
	}

	// Set the desired start address
	offset = 0x0;

	PFN_DPCDREAD pfnDPCDRead = (PFN_DPCDREAD)GetProcAddress(hSysUtilLib, "DPCDRead");

	for (int j = 0; j < enuDisplay.Count; j++)
	{
	targetID = enuDisplay.ConnectedDisplays[j].TargetID;

		if ((pfnDPCDRead)(offset, targetID, dpcdBuffer, BUFFER_SIZE))
		{
			for (int i = 0; i < BUFFER_SIZE; i++)			
				printf("Target Id: %d. DPCD Address: %d. DPCD value: %d \n", targetID, offset + i, dpcdBuffer[i]);
		}
		else
		{
			printf("\n DPCDRead Failed\n");
		   break; // Break from the loop
		}
	}
}
