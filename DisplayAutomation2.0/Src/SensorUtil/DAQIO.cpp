#include <stdio.h>
#include "DAQIO.h"

#pragma comment(lib, "nidaqmx.lib")

DAQIO::DAQIO()
{
    mTaskHandle          = 0;
    mDataOffset          = 0;
    mNumSamplesToCapture = 0;
    mDataBuffer          = NULL;

    memset(mErrBuf, 0, sizeof(mErrBuf));
}

DAQIO::~DAQIO()
{
}

HRESULT DAQIO::CaptureSamples(DWORD AnalogInputIndex, DWORD SamplingRate, DWORD &NumSamplesToCapture, double *pSamples)
{
    HRESULT hr                      = S_OK;
    int32   error                   = 0;
    DWORD   nSamplesRead            = 0;
    BOOL    bErrInCallbackFunction  = FALSE;
    mErrorOccuredInCallbackFunction = 0;
    char devName[32];

    if (NULL == pSamples)
    {
        return E_OUTOFMEMORY;
    }

    mDataOffset          = 0;
    mNumSamplesToCapture = NumSamplesToCapture;
    mDataBuffer          = pSamples;

    mNumSamplesToReadInOneIteration = min(1000, NumSamplesToCapture);

    /*********************************************/
    // DAQmx Configure Code
    /*********************************************/

    sprintf_s(devName, "Dev1/ai%d", AnalogInputIndex);

    DAQmxErrChk(DAQmxCreateTask("", &mTaskHandle));
    DAQmxErrChk(DAQmxCreateAIVoltageChan(mTaskHandle, devName, "", DAQmx_Val_RSE, 0, 5.0, DAQmx_Val_Volts, NULL));
    DAQmxErrChk(DAQmxCfgSampClkTiming(mTaskHandle, "", SamplingRate, DAQmx_Val_Rising, DAQmx_Val_ContSamps, mNumSamplesToReadInOneIteration));
    DAQmxErrChk(DAQmxRegisterEveryNSamplesEvent(mTaskHandle, DAQmx_Val_Acquired_Into_Buffer, mNumSamplesToReadInOneIteration, 0, EveryNSamplesCallback, this));
    DAQmxErrChk(DAQmxStartTask(mTaskHandle));

    while ((nSamplesRead < NumSamplesToCapture) && !bErrInCallbackFunction)
    {
        nSamplesRead           = InterlockedOr(&mDataOffset, 0);
        bErrInCallbackFunction = InterlockedOr(&mErrorOccuredInCallbackFunction, 0);
        Sleep(10);
    }

Error:
    if (DAQmxFailed(error) || bErrInCallbackFunction)
    {
        DAQmxGetExtendedErrorInfo(mErrBuf, ERROR_BUFFER_SIZE);
        printf("DAQmx Error: %s\n", mErrBuf);
        hr = E_FAIL;
    }

    NumSamplesToCapture = nSamplesRead;

    Cleanup();
    return hr;
}

int32 DAQIO::EveryNSamplesCallback(TaskHandle taskHandle, int32 everyNsamplesEventType, uInt32 nSamples, void *callbackData)
{
    DAQIO *pThis = (DAQIO *)callbackData;
    return pThis->SampleCaptureCallback(nSamples);
}

HRESULT DAQIO::SampleCaptureCallback(uInt32 nSamples)
{
    HRESULT hr    = S_OK;
    int32   error = 0;
    int32   NumSamplesRead;

    DWORD samplesAlredayCaptured = InterlockedOr(&mDataOffset, 0);
    DWORD samplesToRead          = min(mNumSamplesToReadInOneIteration, (mNumSamplesToCapture - samplesAlredayCaptured));

    DAQmxErrChk(DAQmxReadAnalogF64(mTaskHandle, samplesToRead, 10.0, DAQmx_Val_GroupByScanNumber, &mDataBuffer[mDataOffset], samplesToRead, &NumSamplesRead, NULL));
    InterlockedAdd(&mDataOffset, NumSamplesRead);

Error:
    if (DAQmxFailed(error))
    {
        DAQmxGetExtendedErrorInfo(mErrBuf, ERROR_BUFFER_SIZE);
        printf("DAQmx Error: %s\n", mErrBuf);
        hr = E_FAIL;
    }

    return hr;
}

void DAQIO::Cleanup(void)
{
    if (mTaskHandle != 0)
    {
        /*********************************************/
        // DAQmx Stop Code
        /*********************************************/
        DAQmxStopTask(mTaskHandle);
        DAQmxClearTask(mTaskHandle);
        mTaskHandle = 0;
    }
}