/**
* @file
* @section SHEUtility_c
* @brief Internal source file which contains implementation required for getting information related to
* SHE harware interfaces related to hot plugin/plugout, Powerline switch(AC/DC) and Lid Switch.
*
* @ref SHEUtility.c
*/

/***********************************************************************************************
* INTEL CONFIDENTIAL. Copyright (c) 2016 Intel Corporation All Rights Reserved.
*  <br>The source code contained or described herein and all documents related to the source code
*  ("Material") are owned by Intel Corporation or its suppliers or licensors. Title to the
*  Material remains with Intel Corporation or its suppliers and licensors. The Material contains
*  trade secrets and proprietary and confidential information of Intel or its suppliers and licensors.
*  The Material is protected by worldwide copyright and trade secret laws and treaty provisions.
*  No part of the Material may be used, copied, reproduced, modified, published, uploaded, posted,
*  transmitted, distributed, or disclosed in any way without Intel’s prior express written permission.
*  <br>No license under any patent, copyright, trade secret or other intellectual property right is
*  granted to or conferred upon you by disclosure or delivery of the Materials, either expressly,
*  by implication, inducement, estoppel or otherwise. Any license under such intellectual property
*  rights must be express and approved by Intel in writing.
*/

#pragma once

/* User include files*/
#include "SHEUtilityDetails.h"

/* Provide DLL version details*/
CDLL_EXPORT bool GetDLLVersion(PULONG pVersion)
{
	/* Check for the error parameter is passed properly,
	this check is done only for exported functions*/
	if (NULL == pVersion)
		return false;

	/* Set current DLL version details*/
	*pVersion = (ULONG)SHE_INTERFACE_VERSION;

	return true;
}
/* It returns type of SHE device connected , configuration of device and Com port number*/
CDLL_EXPORT int GetSHEDeviceTypeandComPort(PINT configuration_type, PINT ComNumber)
{
	int status = 0;

	/* Allocate buffer which contains the details*/
	char* Buffer = (char*)calloc(BUFFERSIZE * sizeof(char), sizeof(char));

	char* DeviceType = (char*)malloc(BUFFERSIZE * sizeof(char));


	/* Check for the error parameter is passed properly,
	this check is done only for exported functions*/
	if (NULL == configuration_type || NULL == Buffer || NULL == DeviceType) {
		free(DeviceType);

		free(Buffer);
		return status;
	}
		

	if (GetcomBufferDetails(ComNumber, Buffer))
	{
		if (strcmp(Buffer, "") != 0)
		{
			if (strcmp(Buffer, "SHE_CONNECTED") == 0)
			{
				status = 1;
			}

			else
			{
				DeviceType = _strdup(Buffer + 7);
				*configuration_type = atoi(DeviceType);
				status = 2;
			}
		}

	}

	free(DeviceType);

	free(Buffer);

	/* Return error if any*/
	return status;

}

/* Display Hotplug unplug  related functionality depending on Opcode*/
CDLL_EXPORT bool HotPlugUnplug(PINT ComNumber, int opcode, int delay)
{
	bool status = false;
	/* Allocate buffer which contains the opcode details*/
	char* pBuffer = (char*)malloc(BUFFERSIZE * sizeof(char));
	if (pBuffer != NULL)
	{
		if (opcode)
		{
			sprintf_s(pBuffer, BUFFERSIZE * sizeof(char), "%d %d", opcode, delay);

			/* Write opcode to the port*/
			if (SerialWrite(pBuffer, (DWORD)strlen(pBuffer), ComNumber))
				status = true;
		}
	}

	/* Do the cleanup*/
	free(pBuffer);

	return status;
}




/*Get the configuration of Connected DiEmPl tool*/
bool GetcomBufferDetails(PINT ComPort, PCHAR Buffer)
{
	/* Initailize local variables*/
	bool status = false;
	char* pComPort = (char*)malloc(BUFFERSIZE * sizeof(char));

	COMMTIMEOUTS timeouts = { 0, //interval timeout. 0 = not used
		0, // read multiplier
		2000, // read constant (milliseconds)
		0, // Write multiplier
		0  // Write Constant
	};

	/*OVERLAPPED ol = { 0 };*/

	/* Validate params*/


	if (pComPort == NULL)
		return status;


	/* Iterate the COM ports to check for the device*/
	for (int count = 1; count < MAXPORTS; count++)
	{
		sprintf_s(pComPort, BUFFERSIZE * sizeof(char), "\\\\.\\COM%d", count);

		/* Open COM port*/
		HANDLE hPort = CreateFile((LPCSTR)pComPort, GENERIC_READ | GENERIC_WRITE, 0, NULL,
			OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

		/* Check the com port handle*/
		if (hPort == INVALID_HANDLE_VALUE)
			continue;
		else
		{
			/* The port was opened successfully*/
			LPCOMMPROP pCommProp = (COMMPROP*)malloc(sizeof(COMMPROP));

			if (pCommProp == NULL)
			{
				CloseHandle(hPort);
				break;
			}


			/* Retrieves the current control settings for a specified com device.*/
			DCB dcbSerialParams = { 0 };
			dcbSerialParams.DCBlength = sizeof(DCB);
			if (GetCommState(hPort, &dcbSerialParams))
			{
				/* Configures com device according to the specifications set in device-control block (a DCB structure)*/
				DWORD noOfBytesRead;
				DWORD noOfBytesToWrite;
				DWORD noOfBytesWritten;
				char* pBuffer = (char*)malloc(BUFFERSIZE * sizeof(char));
				dcbSerialParams.BaudRate = CBR_9600;
				dcbSerialParams.ByteSize = 8;
				dcbSerialParams.StopBits = ONESTOPBIT;
				dcbSerialParams.Parity = NOPARITY;

				
				if (SetCommState(hPort, &dcbSerialParams))
				{
					Sleep(2000);
					noOfBytesRead = 0;
					noOfBytesWritten = 0;
					int opCode = 0;
					int delay = 0;

					if (pBuffer != NULL)
					{
						sprintf_s(pBuffer, BUFFERSIZE * sizeof(char), "%d %d", opCode, delay);
						noOfBytesToWrite = (DWORD)strlen(pBuffer);

						SetCommTimeouts(hPort, &timeouts);

						/* Write data to the com port*/
						if (WriteFile(hPort, pBuffer, noOfBytesToWrite, &noOfBytesWritten, NULL))
						{
							/* Verify if all bytes are written*/
							if (noOfBytesToWrite == noOfBytesWritten)
							{
								noOfBytesRead = 0;
								/* Read data from the com port*/
								if (ReadFile(hPort, Buffer, 13, &noOfBytesRead, NULL))
								{
									if (strcmp(Buffer, "") == 0)
										status = false;

									else
										status = true;

								}

							}
						}
					}
				}
				free(pBuffer);
			}

			/* Release the handle*/

			free(pCommProp);
			CloseHandle(hPort);
			
		}

		/* Check if COM port is connected to device*/
		if (status)
		{
			*ComPort = count;
			break;
		}
	}
	free(pComPort);
	return status;
}

/* Write opCode to the serial com port*/
bool SerialWrite(PCHAR pBuffer, DWORD noOfBytesToWrite, PINT ComNumber)
{
		/* Set operation status*/
		bool status = false;

		char* pComPort = (char *)malloc(BUFFERSIZE * sizeof(char));
		if (pComPort == NULL)
			return status;


		sprintf_s(pComPort, BUFFERSIZE * sizeof(char), "\\\\.\\COM%d", *ComNumber);

		HANDLE hSerial = CreateFile((LPCSTR)pComPort, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

		/* Check for the handle*/
		if (hSerial != INVALID_HANDLE_VALUE)
		{
			/* Retrieves the current control settings for a specified com device.*/
			DCB dcbSerialParams = { 0 };
			dcbSerialParams.DCBlength = sizeof(DCB);
			if (GetCommState(hSerial, &dcbSerialParams))
			{
				/* Configures com device according to the specifications set in device-control block (a DCB structure)*/
				DWORD noOfBytesWritten;
				dcbSerialParams.BaudRate = CBR_9600;
				dcbSerialParams.ByteSize = 8;
				dcbSerialParams.StopBits = ONESTOPBIT;
				dcbSerialParams.Parity = NOPARITY;
				if (SetCommState(hSerial, &dcbSerialParams))
				{
					Sleep(2000);
					noOfBytesWritten = 0;

					/* Write data to the com port*/
					if (WriteFile(hSerial, pBuffer, noOfBytesToWrite, &noOfBytesWritten, NULL))
					{
						Sleep(2000);

						/* Verify if all bytes are written*/
						if (noOfBytesToWrite == noOfBytesWritten)
							status = true;
					}
				}
			}
			/* Close the file handle*/
			CloseHandle(hSerial);
		}
		/* Release memory*/
		free(pComPort);
	//}

	/* Return serial write success status*/
	return status;
}

/* This function is for contious plug/unplug without delay and hibernet*/
CDLL_EXPORT bool DisplayUnplugPLug(PINT ComPort, int opcode1, int opcode2, int delay1, bool LidSwitchPress)
{
	bool status = false;
	/* Allocate buffer which contains the opcode details*/
	char* pBuffer = (char *)malloc(BUFFERSIZE * sizeof(char));
	if (pBuffer != NULL)
	{
		if (LidSwitchPress)
		{
			sprintf_s(pBuffer, BUFFERSIZE * sizeof(char), "%d %d %d %d", opcode1, delay1, opcode2, 15);//send 15 opcode to make hibernate work
			
		}
		else
		{
			sprintf_s(pBuffer, BUFFERSIZE * sizeof(char), "%d %d %d", opcode1, delay1, opcode2);//for contious plug unplug
		}

		if (opcode1 && opcode2)
		{
			/* Write opcode to the port*/
			if (SerialWrite(pBuffer, (DWORD)strlen(pBuffer),ComPort))
				status = true;
		}
	}

	/* Do the cleanup*/
	free(pBuffer);

	return status;
}


