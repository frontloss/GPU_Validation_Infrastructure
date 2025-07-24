// ReadDPCDRegisters.cpp : Defines the entry point for the console application.

#include "stdafx.h"

/* System Includes */
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

/* User Includes*/
#include "ReadDPCDRegisters.h"

#define BUFFER_SIZE 4096

/* Strutures and variables to hold the fetched data*/
HMODULE hSysUtilLib = NULL;
HRESULT errorCode = S_OK;

/* Register to check escape and MMIO read interfaces*/
ULONG ulOffset = 0x70180;
ULONG value = 0;

/* Structures to test the DLL functionalities*/
ENUMERATED_DISPLAYS enuDisplay;

bool DPCDRead(ULONG ulStartOffset, UINT targetID, ULONG ulDpcdBuffer[], UINT dpcdBufferSize);

/* Main entry point*/
int main(int argc, char *argv[])
{
	UINT uiNumOfDPCDs = 0;
	
	do
	{
		if( argc == 2 ) 
		{
			printf("The argument supplied is %s\n", argv[1]);
		}
		else if( argc > 2 ) 
		{
			printf("\nToo many arguments supplied. Usage: %s <Number of DPCD bytes to read>", argv[0] );
			break;
		}
		else 
		{
			printf("\nOne argument expected. Usage: %s <Number of DPCD bytes to read>", argv[0] );
			break;
		}
		
		// Convert DPCD count to int
		uiNumOfDPCDs = atoi(argv[1]);  

		if (uiNumOfDPCDs <= 0 || uiNumOfDPCDs > 4096)
		{
			printf("\n Invalid argument. DPCD number should be in range 1 <-> 4096 bytes\n");
			break;
		}
		
		/* Load and verify */
		hSysUtilLib = LoadSystemUtilityDLL();
		if (NULL == hSysUtilLib)
		{
			printf("\nFailed to Load SystemUtility DLL\n");
			break;
		}

		// Read DPCD registers now
		ReadDPCDRegisters(uiNumOfDPCDs);

	} while (FALSE);

	return 0;
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

void ReadDPCDRegisters(INT uiNumOfDPCDs)
{
	UINT targetID = 0;
	ULONG offset = 0;
	ULONG dpcdBuffer[1];

	enuDisplay.Size = sizeof(ENUMERATED_DISPLAYS);

	PFN_EDISPLAY_INFO_ADD pfnGetEnumDisplay = (PFN_EDISPLAY_INFO_ADD)GetProcAddress(hSysUtilLib, "GetEnumeratedDisplayInfo");
	(pfnGetEnumDisplay)(&enuDisplay, &errorCode);

	printf("\nTotal number of enumerated Displays: %d\n", enuDisplay.Count);
	
	if(enuDisplay.Count <= 0)
	{
		printf("\nDP/eDP display(s) not attached! Attach atleast one DP/eDP display. Exiting... \n");
		return;
	}

	if (errorCode != S_OK)
	{
		printf("\nCheckGetEnumeratedDisplayInfo() returned error code %u\n", errorCode);
		getchar();
	}

	// Set the desired start address
	offset = 0;

	PFN_DPCDREAD pfnDPCDRead = (PFN_DPCDREAD)GetProcAddress(hSysUtilLib, "DPCDRead");

	char szFileName[255] = { 0 };	

	for (int j = 0; j < enuDisplay.Count; j++)
	{
		// Get the target Id
		targetID = enuDisplay.ConnectedDisplays[j].TargetID;

		// Appending target id and display name to the DPCD file name
		sprintf(szFileName, "DPCD_Dump_0x%x_%s.bin", enuDisplay.ConnectedDisplays[j].TargetID, enuDisplay.ConnectedDisplays[j].FriendlyDeviceName);

		FILE *fp = fopen(szFileName, "w");

		if (fp == NULL)
		{
			printf("\nBinary file creation failed! Exiting ...");
			return;
		}

		// Read uiNumOfDPCDs number of DPCDs 
		for (int k = 0; k < uiNumOfDPCDs; k++)
		{
			if ((pfnDPCDRead)(k, targetID, dpcdBuffer, 1))
			{
					printf("Target Id: 0x%x. DPCD Address: %d. DPCD value: %x \n", targetID, offset + k, dpcdBuffer[0]);
					fputc(dpcdBuffer[0], fp);
			}
			else
			{
				printf("\n DPCDRead Failed for address: %d \n", offset + k);
				fclose(fp);
				break; // Break from the loop
			}
		}
		// Close the file handle
		fclose(fp);
	}
}
