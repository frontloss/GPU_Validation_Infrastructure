#include <windows.h>
#include <stdio.h>
#include <Shlwapi.h>
#include "DAQIO.h"
#include "WaveIO.h"

#pragma comment(lib, "Shlwapi")

typedef struct
{
    PWCHAR OutFileName;
    PWCHAR OutWavFileName;
    DWORD  AnalogInputIndex;
    DWORD  SamplingRate;
    double DurationOfCapture;
} SENSOR_APP_CFG;

void PrintUsage(WCHAR *pExeNameWithPath)
{
    WCHAR *pExeName = StrRChrW(pExeNameWithPath, NULL, L'\\');

    if (pExeName)
    {
        pExeName += 1; // Skip '\'
    }
    else
    {
        pExeName = pExeNameWithPath;
    }
    
	wprintf(L"\n\nUsage: %s -i <analog input> -o <output text file> -s <sampling rate> -d <duration in sec> -wav <wav file>", pExeName);
}

INT ParseArguments(int argc, WCHAR *argv[], SENSOR_APP_CFG *pCfg)
{
    if (argc < 5)
    {
        PrintUsage(argv[0]);
        return -1;
    }

    BOOL i = 1;

    while (i < argc)
    {
        if (_wcsicmp(argv[i], L"-i") == 0)
        {
            i++;
            pCfg->AnalogInputIndex = _wtoi(argv[i]);
        }
        else if (_wcsicmp(argv[i], L"-o") == 0)
        {
            i++;
            pCfg->OutFileName = argv[i];
        }
        else if (_wcsicmp(argv[i], L"-wav") == 0)
        {
            i++;
            pCfg->OutWavFileName = argv[i];
        }
        else if (_wcsicmp(argv[i], L"-s") == 0)
        {
            i++;
            pCfg->SamplingRate = _wtoi(argv[i]);
        }
        else if (_wcsicmp(argv[i], L"-d") == 0)
        {
            i++;
            pCfg->DurationOfCapture = _wtof(argv[i]);
        }
        i++;
    }

    return 0;
}

void WriteWaveFile(SENSOR_APP_CFG *pAppCfg, DWORD NumSamplesCaptured, double *pSamplesDouble)
{
    double minVal        = 100.0;
    double average       = 0;
    float *pSamplesFloat = (float *)malloc(2 * NumSamplesCaptured * sizeof(float));

    for (DWORD i = 0; i < NumSamplesCaptured; i++)
    {
        minVal = min(minVal, pSamplesDouble[i]);
        average += pSamplesDouble[i];
    }

    average /= NumSamplesCaptured;

    minVal -= average;
    minVal = -minVal;

    for (DWORD i = 0; i < NumSamplesCaptured; i++)
    {
        pSamplesFloat[2 * i]     = (float)min(pSamplesDouble[i], 1);              // Left channel has original signal
        pSamplesFloat[2 * i + 1] = (float)((pSamplesDouble[i] - average) / minVal); // Right channel has normalized signal
    }

    WaveIO *pWav = new WaveIO();
    pWav->WriteWaveFile(pAppCfg->OutWavFileName, pAppCfg->SamplingRate, 2, NumSamplesCaptured, pSamplesFloat);
    delete pWav;
}

void CaptureSamples(SENSOR_APP_CFG *pAppCfg)
{
    DAQIO *pDaq = new DAQIO();

    DWORD NumSamplesToCapture = (DWORD)(pAppCfg->SamplingRate * pAppCfg->DurationOfCapture);
    DWORD NumSamplesCaptured  = NumSamplesToCapture;

    double *pSamplesDouble = (double *)malloc(NumSamplesToCapture * sizeof(double));

    HRESULT hr = pDaq->CaptureSamples(pAppCfg->AnalogInputIndex, pAppCfg->SamplingRate, NumSamplesCaptured, pSamplesDouble);

    if (NumSamplesCaptured == NumSamplesToCapture)
    {
        printf("!!! SUCCESS !!! Captured %d samples", NumSamplesCaptured);
    }
    else
    {
        printf("!!! ERROR !!! Captured %d samples", NumSamplesCaptured);
    }

    FILE *pF = NULL;
    _wfopen_s(&pF, pAppCfg->OutFileName, L"w");

    if (pF)
    {
        for (DWORD i = 0; i < NumSamplesCaptured; i++)
        {
            fprintf(pF, "%.8f\n", pSamplesDouble[i]);
        }

        fclose(pF);
    }

    if (pAppCfg->OutWavFileName)
    {
        WriteWaveFile(pAppCfg, NumSamplesCaptured, pSamplesDouble);
    }

    delete pDaq;
    free(pSamplesDouble);
}

int wmain(int argc, WCHAR *argv[])
{
    SENSOR_APP_CFG cfg = { 0 };

    if (ParseArguments(argc, argv, &cfg) < 0)
    {
        return -1;
    }

    CaptureSamples(&cfg);

    return 0;
}