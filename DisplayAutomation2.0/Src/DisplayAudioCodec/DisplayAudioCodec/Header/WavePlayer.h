#pragma once

#include <windows.h>
#include <initguid.h>
#include <stdio.h>
#include <Mmdeviceapi.h>
#include <Audioclient.h>

#include "Common.h"
#include "DACVerifier.h"

typedef struct
{
#pragma pack(1)
    UCHAR  chunkID[4];
    DWORD  chunkSize;
    UCHAR  format[4];
    UCHAR  subChunk1Id[4];
    DWORD  subChunk1Size;
    USHORT audioFormat;
    USHORT nChannels;
    DWORD  sampleRate;
    DWORD  byteRate;
    USHORT blockAlign;
    USHORT wBitsPerSample;
    UCHAR  subChunk2Id[4];
    DWORD  subChunk2Size;
#pragma pack()
} WAVE_HDR;

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
#pragma pack()
} WAVE_HDR_EX2;

class WavePlayer
{
  public:
    WavePlayer(PWCHAR endpointName, PORT_TYPE endpointPortType, PWCHAR fileToPLay, BOOL bListen, BOOL bVerify);
    ~WavePlayer();
    HRESULT PlayWaveFile(PGFX_ADAPTER_INFO pAdapterInfo = NULL);

  private:
    WAVE_HDR_EX2 mHdrEx;
    BOOL         mbVerify;
    BOOL         mbListen;
    FILE *       mFile;
    UINT64       mNumFramesInFile;
    UINT64       mNumBytesInFile;
    UINT64       mNumBytesRemainingInFile;
    UINT64       mNumBytesPlayed;
    UINT64       mDurationOfFileInMs;

    DWORD mBitsPerSampleInFile;
    BYTE  mTmpBuffer[10 * 1024 * 1024]; // 10 MB

    HRESULT mPlayerThreadExitCode;

    IMMDevice *mAudioDevice;
    PORT_TYPE  mAudioEndpointPortType;
    WCHAR      mAudioEndpointName[MAX_STR_LEN];
    WCHAR      mMediaFileName[MAX_STR_LEN];

    BOOL IsFileHeaderValid();
    BOOL ReadWavFileHeader();
    BOOL CheckAudioEndPointPresence();

    HRESULT IntializeFileReader();
    HRESULT ReadSamplesFromFile(DWORD NumBytesToRead, PBYTE pSamples);
    HRESULT FindSupportedSpeakerConfiguration(WAVEFORMATEXTENSIBLE *pFmt, IAudioClient *pAudioClient);
    HRESULT PlayFileAndVerify(PGFX_ADAPTER_INFO pAdapterInfo);
    HRESULT PlayFile();

    void GetWavDataSize();
    void RemapSpeakers(WAVEFORMATEXTENSIBLE *pFmt);
    void ReconstructWaveHeader(WAVEFORMATEXTENSIBLE *pFmt);

    static DWORD PlayerThread(LPVOID pParams);
};
