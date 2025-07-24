/*------------------------------------------------------------------------------------------------*
 *
 * @file     SensorDataCapture.h
 * @brief    Header file for SensorDataCapture.cpp
 * @author   ashishk2
 *
 *------------------------------------------------------------------------------------------------*/
#pragma once
#include <windows.h>
#include <stdio.h>
#include "DAQIO.h"

#pragma comment(lib, "Logger.lib")
char LIBRARY_NAME[] = "SensorUtil.dll";

typedef struct
{
	DWORD  AnalogInputIndex;
	DWORD  SamplingRate;
	double DurationOfCapture;
}SENSOR_INFO;

/**---------------------------------------------------------------------------------------------------------*
 * Description:         This function captures optical sensor data
 * @param[In]           pSensorInfo : This contains sensor config data
 * @param[In]           samplesData[] : Captures sensor data in it, shared by caller
 * @param[In]           sampleSize    : length of the samplesData
 * return:              BOOL.  'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 *----------------------------------------------------------------------------------------------------------*/
extern "C" __declspec(dllexport) BOOL __cdecl CaptureSensorData(SENSOR_INFO *pSensorInfo, double samplesData[], int sampleSize);

