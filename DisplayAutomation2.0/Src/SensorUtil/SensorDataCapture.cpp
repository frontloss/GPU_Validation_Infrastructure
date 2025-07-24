/*------------------------------------------------------------------------------------------------*
 *
 * @file     SensorDataCapture.cpp
 * @brief    This file captures sensor data based on config provided in SENSOR_INFO
 *           and provides it to caller. 
 * @author   ashishk2
 *
 *------------------------------------------------------------------------------------------------*/
#include "SensorDataCapture.h"


/**---------------------------------------------------------------------------------------------------------*
 * @brief               CaptureSensorData
 * Description:         This function captures optical sensor data.
 * @param[In]           pSensorInfo : This contains Sensor config information
 * @param[In]           samplesData[] : captures sensor data in it, shared by caller
 * @param[In]           sampleSize    : length of the samplesData
 * return:              BOOL.  'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 *----------------------------------------------------------------------------------------------------------*/
BOOL CaptureSensorData(SENSOR_INFO *pSensorInfo, double samplesData[], int sampleSize)
{
	if (pSensorInfo == nullptr)
	{
		ERROR_LOG("pSensorInfo is NULL");
		return FALSE;
	}

	DWORD NumSamplesToCapture = (DWORD)(pSensorInfo->SamplingRate * pSensorInfo->DurationOfCapture);
	DWORD NumSamplesCaptured = NumSamplesToCapture;

	if (sampleSize != NumSamplesToCapture)
	{
		ERROR_LOG("SamplesSize :%d not matching with NumSamplesToCapture:%lu", sampleSize, NumSamplesToCapture);
		return FALSE;
	}

	BOOL bStatus = TRUE;
	DAQIO *pDaq = new DAQIO();
	
	HRESULT hr = pDaq->CaptureSamples(pSensorInfo->AnalogInputIndex, pSensorInfo->SamplingRate, NumSamplesCaptured, samplesData);

	if (hr != S_OK)
	{
		ERROR_LOG("!!! ERROR !!! CaptureSamples Failed: %ld", hr);
		bStatus = FALSE;
	}

	if (NumSamplesCaptured == NumSamplesToCapture)
	{
		INFO_LOG("!!! SUCCESS !!! Captured %lu samples", NumSamplesCaptured);
	}
	else
	{
		ERROR_LOG("!!! ERROR !!! Captured %lu samples", NumSamplesCaptured);
		bStatus = FALSE;
	}

	delete pDaq;
	return bStatus;
}