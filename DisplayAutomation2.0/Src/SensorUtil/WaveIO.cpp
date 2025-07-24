#include "WaveIO.h"
#include "log.h"

WaveIO::WaveIO()
{
    mSampleDataSize = 0;
    memset(&mWavHdr, 0, sizeof(mWavHdr));
}

WaveIO::~WaveIO()
{
}

void WaveIO::InitializeWaveHeaderFloat(DWORD nSamplesPerChennel, DWORD nSamplingRate, DWORD nChannels)
{
    memset(&mWavHdr, 0, sizeof(mWavHdr));

    memcpy(mWavHdr.chunkID, "RIFF", 4);
    memcpy(mWavHdr.format, "WAVE", 4);
    memcpy(mWavHdr.subChunk1Id, "fmt ", 4);
    memcpy(mWavHdr.subChunk2Id, "data", 4);

    mWavHdr.subChunk1Size       = sizeof(WAVEFORMATEX);
    mWavHdr.waveFormatEx.cbSize = 0;

    mWavHdr.waveFormatEx.wFormatTag      = WAVE_FORMAT_IEEE_FLOAT;
    mWavHdr.waveFormatEx.nChannels       = (WORD)nChannels;
    mWavHdr.waveFormatEx.nSamplesPerSec  = nSamplingRate;
    mWavHdr.waveFormatEx.wBitsPerSample  = 32;
    mWavHdr.waveFormatEx.nBlockAlign     = (WORD)((nChannels * mWavHdr.waveFormatEx.wBitsPerSample) / 8);
    mWavHdr.waveFormatEx.nAvgBytesPerSec = mWavHdr.waveFormatEx.nBlockAlign * nSamplingRate;

    mSampleDataSize       = nSamplesPerChennel * (mWavHdr.waveFormatEx.wBitsPerSample / 8) * nChannels;
    mWavHdr.subChunk2Size = mSampleDataSize;
    mWavHdr.chunkSize     = sizeof(mWavHdr) + mSampleDataSize - 8;
}

void WaveIO::RemapSpeakers(WAVEFORMATEXTENSIBLE *pFmt)
{
    switch (pFmt->Format.nChannels)
    {
    case 1:
        pFmt->dwChannelMask = SPEAKER_FRONT_CENTER;
        break;
    case 2:
        pFmt->dwChannelMask = (SPEAKER_FRONT_LEFT | SPEAKER_FRONT_RIGHT);
        break;
    case 4:
        pFmt->dwChannelMask = (SPEAKER_FRONT_LEFT | SPEAKER_FRONT_RIGHT | SPEAKER_BACK_LEFT | SPEAKER_BACK_RIGHT);
        break;
    case 6:
        pFmt->dwChannelMask = (SPEAKER_FRONT_LEFT | SPEAKER_FRONT_RIGHT | SPEAKER_FRONT_CENTER | SPEAKER_LOW_FREQUENCY | SPEAKER_SIDE_LEFT | SPEAKER_SIDE_RIGHT);
        break;
    case 8:
        pFmt->dwChannelMask =
        (SPEAKER_FRONT_LEFT | SPEAKER_FRONT_RIGHT | SPEAKER_FRONT_CENTER | SPEAKER_LOW_FREQUENCY | SPEAKER_BACK_LEFT | SPEAKER_BACK_RIGHT | SPEAKER_SIDE_LEFT | SPEAKER_SIDE_RIGHT);
        break;
    default:
        printf("Incorrect input");
    }
}

HRESULT WaveIO::WriteWaveFile(const PWCHAR pWavFileName, DWORD SamplingRate, DWORD NumChannels, DWORD NumSamplesPerChannel, float *pSampleData)
{
    FILE *  pF = NULL;
    HRESULT hr = S_OK;

    _wfopen_s(&pF, pWavFileName, L"wb");

    if (pF)
    {
        InitializeWaveHeaderFloat(NumSamplesPerChannel, SamplingRate, NumChannels);

        fwrite(&mWavHdr, 1, sizeof(mWavHdr), pF);
        fwrite(pSampleData, 1, mSampleDataSize, pF);
        fclose(pF);
    }
    else
    {
        hr = ERROR_FILE_INVALID;
    }
    return hr;
}
