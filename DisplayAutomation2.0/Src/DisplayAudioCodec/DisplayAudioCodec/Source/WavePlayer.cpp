#pragma once

#include <windows.h>
#include <Mmdeviceapi.h>
#include <Audioclient.h>
#include <Functiondiscoverykeys_devpkey.h>
// #include "<framework.h>"
#include "..\Header\WavePlayer.h"
#include "..\Header\DisplayAudioCodec.h"
#include "..\Header\Common.h"
#include "..\..\Logger\log.h"
#pragma warning(disable : 4996)
const CLSID CLSID_MMDeviceEnumerator = __uuidof(MMDeviceEnumerator);
const IID   IID_IMMDeviceEnumerator  = __uuidof(IMMDeviceEnumerator);
const IID   IID_IAudioRenderClient   = __uuidof(IAudioRenderClient);
const IID   IID_IAudioClient         = __uuidof(IAudioClient);

WavePlayer::WavePlayer(PWCHAR endpointName, PORT_TYPE endpointPortType, PWCHAR fileToPLay, BOOL bListen, BOOL bVerify)
{
    mbVerify              = bVerify;
    mbListen              = bListen;
    mFile                 = NULL;
    mAudioDevice          = NULL;
    mPlayerThreadExitCode = S_OK;

    mNumFramesInFile         = 0;
    mNumBytesInFile          = 0;
    mNumBytesRemainingInFile = 0;

    memset(&mHdrEx, 0, sizeof(mHdrEx));

    mAudioEndpointPortType = endpointPortType;

    wcscpy(mMediaFileName, fileToPLay);
    wcscpy(mAudioEndpointName, endpointName);
}

WavePlayer::~WavePlayer()
{
    if (mFile)
    {
        fclose(mFile);
    }

    SAFE_RELEASE(mAudioDevice);
}

HRESULT WavePlayer::PlayWaveFile(PGFX_ADAPTER_INFO pAdapterInfo)
{
    WCHAR   outMsg[256]   = { 0 };
    HRESULT hr            = E_FAIL;
    BOOL    bConfirmation = TRUE;

    CoInitialize(NULL);

    if (!CheckAudioEndPointPresence())
    {
        ERROR_LOG("%s Device not found %ws", ERROR_MESSAGE, mAudioEndpointName);
        return ERROR_DEVICE_NOT_AVAILABLE;
    }

    if (mbListen)
    {
        wprintf(L"Playing file %s. Type y if sound is heard\n", mMediaFileName);
    }

    if (mbVerify)
    {
        hr = PlayFileAndVerify(pAdapterInfo);
    }
    else
    {
        hr = PlayFile();
    }

    if (mbListen)
    {
        WCHAR ch = _getwch();

        if ((ch != L'Y') && (ch != L'y'))
        {
            bConfirmation = FALSE;
        }
    }

    if ((S_OK == hr) && bConfirmation)
    {
        INFO_LOG("Playback %s", SUCCESS_MESSAGE);
    }
    else
    {
        ERROR_LOG("Playback %s", ERROR_MESSAGE);
    }
    CoUninitialize();
    return hr;
}

BOOL WavePlayer::IsFileHeaderValid()
{
    BOOL bHeaderValid = FALSE;

    if (memcmp(mHdrEx.chunkID, "RIFF", 4) != 0)
    {
        return bHeaderValid;
    }

    if (memcmp(mHdrEx.format, "WAVE", 4) != 0)
    {
        return bHeaderValid;
    }

    if (memcmp(mHdrEx.subChunk1Id, "fmt ", 4) != 0)
    {
        return bHeaderValid;
    }

    if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_PCM)
    {
        WAVE_HDR *pHdr             = (WAVE_HDR *)&mHdrEx;
        UINT8 *   pAddrOfDataBlock = (UINT8 *)&pHdr->subChunk1Size;
        pAddrOfDataBlock += sizeof(DWORD) + pHdr->subChunk1Size;

        if (memcmp(pAddrOfDataBlock, "data", 4) != 0)
        {
            return bHeaderValid;
        }
    }
    else if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_EXTENSIBLE)
    {
        UINT8 *pAddrOfDataBlock = (UINT8 *)&mHdrEx.subChunk1Size;
        pAddrOfDataBlock += sizeof(mHdrEx.subChunk1Size) + mHdrEx.subChunk1Size;

        if (memcmp(pAddrOfDataBlock, "data", 4) != 0)
        {
            return bHeaderValid;
        }
    }

    return TRUE;
}

BOOL WavePlayer::ReadWavFileHeader()
{
    fread(&mHdrEx, 1, sizeof(WAVE_HDR), mFile);

    if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_EXTENSIBLE)
    {
        fseek(mFile, 0, SEEK_SET);
        fread(&mHdrEx, 1, sizeof(WAVE_HDR_EX2), mFile);

        // Invalid cbSize. Correct it.
        if (mHdrEx.waveFormatEx.Format.cbSize != (sizeof(WAVEFORMATEXTENSIBLE) - sizeof(WAVEFORMATEX)))
        {
            mHdrEx.waveFormatEx.Format.cbSize = sizeof(WAVEFORMATEXTENSIBLE) - sizeof(WAVEFORMATEX);
        }
    }
    else if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_PCM)
    {
        fseek(mFile, 0, SEEK_SET);
        fread(&mHdrEx, 1, sizeof(WAVE_HDR), mFile);
    }

    return IsFileHeaderValid();
}

void WavePlayer::GetWavDataSize()
{
    UINT8 *pAddrOfDataSize = NULL;

    if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_EXTENSIBLE)
    {
        pAddrOfDataSize = (UINT8 *)&mHdrEx.subChunk1Size;
        pAddrOfDataSize += sizeof(mHdrEx.subChunk1Size) + mHdrEx.subChunk1Size + 4;
        mNumBytesInFile  = pAddrOfDataSize[0] | (pAddrOfDataSize[1] << 8) | (pAddrOfDataSize[2] << 16) | (pAddrOfDataSize[3] << 24);
        mNumFramesInFile = 8 * mNumBytesInFile / (mHdrEx.waveFormatEx.Format.nChannels * mHdrEx.waveFormatEx.Format.wBitsPerSample);
    }
    else if (mHdrEx.waveFormatEx.Format.wFormatTag == WAVE_FORMAT_PCM)
    {
        WAVE_HDR *pHdr  = (WAVE_HDR *)&mHdrEx;
        pAddrOfDataSize = (UINT8 *)&pHdr->subChunk1Size;
        pAddrOfDataSize += sizeof(pHdr->subChunk1Size) + pHdr->subChunk1Size + 4;
        mNumBytesInFile  = pAddrOfDataSize[0] | (pAddrOfDataSize[1] << 8) | (pAddrOfDataSize[2] << 16) | (pAddrOfDataSize[3] << 24);
        mNumFramesInFile = 8 * mNumBytesInFile / (pHdr->nChannels * pHdr->wBitsPerSample);
    }

    mNumBytesRemainingInFile = mNumBytesInFile;
    mDurationOfFileInMs      = mNumBytesRemainingInFile / (mHdrEx.waveFormatEx.Format.nChannels * mHdrEx.waveFormatEx.Format.wBitsPerSample / 8);
    mDurationOfFileInMs      = (mDurationOfFileInMs * 1000) / mHdrEx.waveFormatEx.Format.nSamplesPerSec;
}

void WavePlayer::RemapSpeakers(WAVEFORMATEXTENSIBLE *pFmt)
{
    switch (pFmt->Format.nChannels)
    {
    case 1:
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_MONO;
        break;
    case 2:
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_STEREO;
        break;
    case 4:
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_QUAD;
        break;
    case 6:
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_5POINT1_SURROUND;
        break; // TODO: Query capability and fill
    case 8:
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_7POINT1_SURROUND;
        break;
    }
}

void WavePlayer::ReconstructWaveHeader(WAVEFORMATEXTENSIBLE *pFmt)
{
    pFmt->Format.wFormatTag = WAVE_FORMAT_EXTENSIBLE;
    pFmt->SubFormat         = KSDATAFORMAT_SUBTYPE_PCM;
    pFmt->Format.cbSize     = sizeof(WAVEFORMATEXTENSIBLE) - sizeof(WAVEFORMATEX);

    pFmt->Samples.wValidBitsPerSample = pFmt->Format.wBitsPerSample;

    if (pFmt->Format.wBitsPerSample > 16)
    {
        pFmt->Format.wBitsPerSample = 32;
    }

    pFmt->Format.nBlockAlign     = pFmt->Format.nChannels * (pFmt->Format.wBitsPerSample / 8);
    pFmt->Format.nAvgBytesPerSec = pFmt->Format.nBlockAlign * pFmt->Format.nSamplesPerSec;

    RemapSpeakers(pFmt);
}

HRESULT WavePlayer::IntializeFileReader()
{
    _wfopen_s(&mFile, mMediaFileName, L"rb");

    if (!mFile)
    {
        ERROR_LOG("%s Could not open file: %s", ERROR_MESSAGE, mMediaFileName);
        return ERROR_FILE_EXISTS;
    }

    BOOL bRetVal = ReadWavFileHeader();

    if (!bRetVal)
    {
        ERROR_LOG("%s Unspupported file fromat: %s", ERROR_MESSAGE, mMediaFileName);
        return E_UNSUPPORTED_TYPE;
    }

    GetWavDataSize();

    mBitsPerSampleInFile = mHdrEx.waveFormatEx.Format.wBitsPerSample;
    ReconstructWaveHeader(&mHdrEx.waveFormatEx);

    return S_OK;
}

HRESULT WavePlayer::ReadSamplesFromFile(DWORD NumBytesToRead, PBYTE pSamples)
{
    if (24 == mBitsPerSampleInFile)
    {
        // 24 bit data will be stored in 32 bit container while playing. However, the file stored data in 24 bit.
        NumBytesToRead = (NumBytesToRead * 3) / 4;
        NumBytesToRead = (DWORD)min(NumBytesToRead, mNumBytesRemainingInFile);
        NumBytesToRead = min(NumBytesToRead, sizeof(mTmpBuffer));

        DWORD NumBytesRead = (DWORD)fread(mTmpBuffer, 1, NumBytesToRead, mFile);

        // Pad 0s if less number of bytes read than requested.
        memset(&mTmpBuffer[NumBytesRead], 0, (NumBytesToRead - NumBytesRead));

        mNumBytesRemainingInFile -= NumBytesRead;

        INT32 *pOutSamples = (INT32 *)pSamples;

        for (DWORD i = 0; i < (NumBytesRead / 3); i++)
        {
            INT32 data = (INT32)mTmpBuffer[3 * i] | ((INT32)mTmpBuffer[3 * i + 1] << 8) | ((INT32)mTmpBuffer[3 * i + 2] << 16);
            data       = data << 8;

            pOutSamples[i] = data;
        }

        return S_OK;
    }

    NumBytesToRead     = (DWORD)min(NumBytesToRead, mNumBytesRemainingInFile);
    DWORD NumBytesRead = (DWORD)fread(pSamples, 1, NumBytesToRead, mFile);

    // Pad 0s if less number of bytes read than requested.
    memset(&pSamples[NumBytesRead], 0, (NumBytesToRead - NumBytesRead));

    mNumBytesRemainingInFile -= NumBytesRead;

    return S_OK;
}

HRESULT WavePlayer::FindSupportedSpeakerConfiguration(WAVEFORMATEXTENSIBLE *pFmt, IAudioClient *pAudioClient)
{
    if (S_OK == pAudioClient->IsFormatSupported(AUDCLNT_SHAREMODE_EXCLUSIVE, (WAVEFORMATEX *)pFmt, NULL))
    {
        return S_OK;
    }

    if (6 == pFmt->Format.nChannels)
    {
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_5POINT1;
    }
    else if (8 == pFmt->Format.nChannels)
    {
        pFmt->dwChannelMask = KSAUDIO_SPEAKER_7POINT1;
        if (S_OK == pAudioClient->IsFormatSupported(AUDCLNT_SHAREMODE_EXCLUSIVE, (WAVEFORMATEX *)pFmt, NULL))
        {
            return S_OK;
        }

        pFmt->dwChannelMask = KSAUDIO_SPEAKER_7POINT0;
    }

    return pAudioClient->IsFormatSupported(AUDCLNT_SHAREMODE_EXCLUSIVE, (WAVEFORMATEX *)pFmt, NULL);
}

DWORD WavePlayer::PlayerThread(LPVOID pParams)
{
    WavePlayer *pThis = (WavePlayer *)pParams;
    HRESULT     hr    = pThis->PlayFile();

    return hr;
}

HRESULT WavePlayer::PlayFile()
{
    UINT32              bufferFrameCount     = 0;
    BYTE *              pBufferData          = NULL;
    REFERENCE_TIME      hnsRequestedDuration = (REFTIMES_PER_SEC / 2); // Allocate buffer for 0.5 sec.
    IAudioClient *      pClient              = NULL;
    IAudioRenderClient *pRenderClient        = NULL;
    HRESULT             hr                   = E_FAIL;
    UINT32              numFramesPadding     = 0;
    DWORD               bytesToBeFilled      = 0;
    DWORD               durationOfBuffer     = 0;

    CoInitialize(NULL);

    // TODO: File read in chunks
    if (wcsstr(mMediaFileName, L".wav"))
    {
        hr = IntializeFileReader();
    }

    EXIT_ON_ERROR(hr);

    mNumBytesPlayed = 0;

    // OS provides buffer for hnsRequestedDuration in case of stereo. Higher nuber of channel will require more data.
    hnsRequestedDuration = (2 * hnsRequestedDuration) / mHdrEx.waveFormatEx.Format.nChannels;

    hr = mAudioDevice->Activate(IID_IAudioClient, CLSCTX_ALL, NULL, (void **)&pClient);
    EXIT_ON_ERROR(hr);

    hr = FindSupportedSpeakerConfiguration(&mHdrEx.waveFormatEx, pClient);

    if (AUDCLNT_E_UNSUPPORTED_FORMAT == hr)
    {
        ERROR_LOG("%s Unsupported stream format.", VERIFICATION_OR_TEST_FAILURE);
    }

    EXIT_ON_ERROR(hr);

    hr = pClient->Initialize(AUDCLNT_SHAREMODE_EXCLUSIVE, 0, hnsRequestedDuration, 0, (WAVEFORMATEX *)&mHdrEx.waveFormatEx, NULL);
    EXIT_ON_ERROR(hr);

    hr = pClient->GetBufferSize(&bufferFrameCount);
    EXIT_ON_ERROR(hr);

    hr = pClient->GetService(IID_IAudioRenderClient, (void **)&pRenderClient);
    EXIT_ON_ERROR(hr);

    // Grab the entire buffer for the initial fill operation.
    hr = pRenderClient->GetBuffer(bufferFrameCount, &pBufferData);
    EXIT_ON_ERROR(hr);

    bytesToBeFilled  = bufferFrameCount * mHdrEx.waveFormatEx.Format.nChannels * mHdrEx.waveFormatEx.Format.wBitsPerSample / 8;
    durationOfBuffer = (1000 * bufferFrameCount) / mHdrEx.waveFormatEx.Format.nSamplesPerSec;

    hr = ReadSamplesFromFile(bytesToBeFilled, pBufferData);
    EXIT_ON_ERROR(hr);

    mNumBytesPlayed += bytesToBeFilled;

    hr = pRenderClient->ReleaseBuffer(bufferFrameCount, 0);
    EXIT_ON_ERROR(hr);

    hr = pClient->Start();
    EXIT_ON_ERROR(hr);

    while (mNumBytesRemainingInFile)
    {
        Sleep(durationOfBuffer / 2);

        hr = pClient->GetCurrentPadding(&numFramesPadding);
        EXIT_ON_ERROR(hr);

        UINT32 numFramesAvailable = bufferFrameCount - numFramesPadding;

        // See how much buffer space is available.
        hr = pRenderClient->GetBuffer(numFramesAvailable, &pBufferData);
        EXIT_ON_ERROR(hr);

        bytesToBeFilled = numFramesAvailable * mHdrEx.waveFormatEx.Format.nChannels * mHdrEx.waveFormatEx.Format.wBitsPerSample / 8;
        hr              = ReadSamplesFromFile(bytesToBeFilled, pBufferData);
        EXIT_ON_ERROR(hr);

        mNumBytesPlayed += bytesToBeFilled;

        hr = pRenderClient->ReleaseBuffer(numFramesAvailable, 0);
        EXIT_ON_ERROR(hr);
    }

    do // Wait for last buffer to complete
    {
        hr = pClient->GetCurrentPadding(&numFramesPadding);
        Sleep(10);
        EXIT_ON_ERROR(hr);
    } while (numFramesPadding);

    pClient->Stop();

Exit:

    SAFE_RELEASE(pClient);
    SAFE_RELEASE(pRenderClient);

    if ((S_OK != hr) && (AUDCLNT_E_UNSUPPORTED_FORMAT != hr))
    {
        INFO_LOG("%s Playback failure", ERROR_MESSAGE);
    }

    mPlayerThreadExitCode = hr;

    CoUninitialize();

    return hr;
}

HRESULT WavePlayer::PlayFileAndVerify(PGFX_ADAPTER_INFO pAdapterInfo)
{
    HRESULT      hr           = S_OK;
    WCHAR        outMsg[256]  = { 0 };
    DACVerifier *pDacVerifier = new DACVerifier();

    DWORD FileDurationInMs = (DWORD)(((double)mNumFramesInFile * 1000) / (double)mHdrEx.waveFormatEx.Format.nSamplesPerSec);

    INFO_LOG("Playing %ws", mMediaFileName);

    hr = pDacVerifier->Initialize(mAudioEndpointName, mAudioEndpointPortType, pAdapterInfo);

    if (S_OK != hr)
    {
        ERROR_LOG("%s Could not initialize DacHandler", ERROR_MESSAGE);
        return FALSE;
    }

    DWORD  ProcessThreadId;
    DWORD  TerminateReason;
    HANDLE threadHandle = CreateThread(NULL, 0, PlayerThread, this, 0, &ProcessThreadId);

    if (0 == threadHandle)
    {
        ERROR_LOG("%s Could not create player thread", ERROR_MESSAGE);
        return FALSE;
    }

    Sleep(200);

    if (S_OK != mPlayerThreadExitCode)
    {
        hr = mPlayerThreadExitCode;
        goto Exit;
    }

    hr = pDacVerifier->VerifyDacProgramming(&mHdrEx.waveFormatEx);
    EXIT_ON_ERROR(hr);

    FileDurationInMs = (DWORD)(((double)mNumFramesInFile * 1000) / (double)mHdrEx.waveFormatEx.Format.nSamplesPerSec);

    TerminateReason = WaitForSingleObject(threadHandle, (FileDurationInMs + 5000)); // Waiting for file duration + 5 sec additional

    if (WAIT_TIMEOUT == TerminateReason)
    {
        ERROR_LOG("%s Player thread timeout. Expeted: %.2f sec, Waited: %.2f sec.", VERIFICATION_FAILURE, ((double)FileDurationInMs / 1000.0),
                  (double)(FileDurationInMs + 5000) / 1000.0);

        hr = ERROR_TIMEOUT;
        goto Exit;
    }

    hr = pDacVerifier->VerifyFinalState(mNumBytesPlayed);

Exit:
    delete pDacVerifier;

    return hr;
}

BOOL WavePlayer::CheckAudioEndPointPresence()
{
    BOOL                 bEndPointPresent = FALSE;
    HRESULT              hr               = S_OK;
    IMMDeviceEnumerator *pEnumerator      = NULL;
    IMMDeviceCollection *pCollection      = NULL;
    IMMDevice *          pAudioDevice     = NULL;
    IPropertyStore *     pProps           = NULL;
    DWORD                nEndpOintsFound  = 0;
    PORT_TYPE            portTypeFound    = PORT_TYPE_MAX;

    CoInitialize(NULL);

    hr = CoCreateInstance(CLSID_MMDeviceEnumerator, NULL, CLSCTX_ALL, IID_IMMDeviceEnumerator, (void **)&pEnumerator);
    EXIT_ON_ERROR(hr);

    hr = pEnumerator->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &pCollection);
    EXIT_ON_ERROR(hr);

    hr = pCollection->GetCount((UINT *)&nEndpOintsFound);
    EXIT_ON_ERROR(hr);

    if (nEndpOintsFound == 0)
    {
        goto Exit;
    }

    // Each loop prints the name of an endpoint device.
    for (ULONG i = 0; (i < nEndpOintsFound) && !bEndPointPresent; i++)
    {
        // Get pointer to endpoint number i.
        hr = pCollection->Item(i, &pAudioDevice);
        CONTINUE_ON_ERROR(hr);

        hr = pAudioDevice->OpenPropertyStore(STGM_READ, &pProps);
        CONTINUE_ON_ERROR(hr);

        PROPVARIANT varName;
        // Initialize container for property value.
        PropVariantInit(&varName);

        // Get the endpoint's friendly-name property.
        hr = pProps->GetValue(PKEY_Device_DeviceDesc, &varName);
        CONTINUE_ON_ERROR(hr);

        if (!_wcsicmp(varName.pwszVal, mAudioEndpointName))
        {
            if (mAudioEndpointPortType != PORT_TYPE_ANALOG)
            {
                PROPVARIANT jackType;
                // Initialize container for property value.
                PropVariantInit(&jackType);

                // Get the endpoint's friendly-name property.
                hr = pProps->GetValue(PKEY_AudioEndpoint_JackSubType, &jackType);
                CONTINUE_ON_ERROR(hr);

                if (!_wcsicmp(jackType.pwszVal, NODETYPE_HDMI_INTERFACE))
                {
                    portTypeFound = PORT_TYPE_HDMI;
                }
                else if (!_wcsicmp(jackType.pwszVal, NODETYPE_DISPLAYPORT_INTERFACE))
                {
                    portTypeFound = PORT_TYPE_DP;
                }
            }
            else // Ignore port type in case of analog ports
            {
                portTypeFound = PORT_TYPE_ANALOG;
            }

            if (portTypeFound == mAudioEndpointPortType)
            {
                bEndPointPresent = TRUE;
                mAudioDevice     = pAudioDevice;
            }
        }
    }

Exit:

    SAFE_RELEASE(pEnumerator);
    SAFE_RELEASE(pCollection);
    SAFE_RELEASE(pProps);

    CoUninitialize();

    return bEndPointPresent;
}
