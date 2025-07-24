#pragma once

#include <windows.h>
#include <mmreg.h>

typedef struct
{
#pragma pack(1)
    UCHAR        chunkID[4];
    DWORD        chunkSize;
    UCHAR        format[4];
    UCHAR        subChunk1Id[4];
    DWORD        subChunk1Size;
    WAVEFORMATEX waveFormatEx;
    UCHAR        subChunk2Id[4];
    DWORD        subChunk2Size;
#pragma pack()
} WAVE_HDR_EX;

typedef struct
{
#pragma pack(1)
    UCHAR                chunkID[4];
    DWORD                chunkSize;
    UCHAR                format[4];
    UCHAR                subChunk1Id[4];
    DWORD                subChunk1Size;
    WAVEFORMATEXTENSIBLE waveFormatEx;
    UCHAR                subChunk2Id[4];
    DWORD                subChunk2Size;
    DWORD                sampleLength;
    UCHAR                subChunk3Id[4];
    DWORD                subChunk3Size;
#pragma pack()
} WAVE_HDR_EX2;

class WaveIO
{
  public:
    WaveIO();
    ~WaveIO();
    HRESULT WriteWaveFile(const PWCHAR pWavFileName, DWORD SamplingRate, DWORD NumChannels, DWORD NumSamplesPerChannel, float *pSampleData);

  private:
    WAVE_HDR_EX mWavHdr;
    DWORD       mSampleDataSize;

    void InitializeWaveHeaderFloat(DWORD nSamplesPerChennel, DWORD nSamplingRate, DWORD nChannels);
    void RemapSpeakers(WAVEFORMATEXTENSIBLE *pFmt);
};