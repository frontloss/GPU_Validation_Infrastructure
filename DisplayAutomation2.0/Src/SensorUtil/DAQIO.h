#pragma once
#include <windows.h>
#include <NIDAQmx.h>
#include "log.h"

#define DAQmxErrChk(functionCall)            \
    if (DAQmxFailed(error = (functionCall))) \
        goto Error;                          \
    else

#define ERROR_BUFFER_SIZE 2048

class DAQIO
{
  public:
    DAQIO();
    ~DAQIO();

    HRESULT CaptureSamples(DWORD AnalogInputIndex, DWORD SamplingRate, DWORD &NumSamplesToCapture, double *pSamples);

  private:
    static int32 CVICALLBACK EveryNSamplesCallback(TaskHandle taskHandle, int32 everyNsamplesEventType, uInt32 nSamples, void *callbackData);
    HRESULT                  SampleCaptureCallback(uInt32 nSamples);

    void Cleanup(void);

    CHAR       mErrBuf[ERROR_BUFFER_SIZE];
    TaskHandle mTaskHandle;
    LONG       mDataOffset;
    LONG       mErrorOccuredInCallbackFunction;
    DWORD      mNumSamplesToCapture;
    DWORD      mNumSamplesToReadInOneIteration;
    double *   mDataBuffer;
};
