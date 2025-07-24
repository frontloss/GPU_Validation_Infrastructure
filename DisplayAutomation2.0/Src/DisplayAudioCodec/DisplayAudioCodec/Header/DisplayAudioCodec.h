// pch.h: This is a precompiled header file.
// Files listed below are compiled only once, improving build performance for future builds.
// This also affects IntelliSense performance, including code completion and many code browsing features.
// However, files listed here are ALL re-compiled if any one of them is updated between builds.
// Do not add files here that you will be updating frequently as this negates the performance advantage.
#pragma once

// add headers that you want to pre-compile here

#define DLLEXPORT extern "C" __declspec(dllexport)
#define DLLVERSION 100
#include <Windows.h>
#include "GFXMMIO.h"
#include <winnt.h>
#include <iostream>
#include <corecrt_wstring.h>
#include <Mmdeviceapi.h>
#include <Functiondiscoverykeys_devpkey.h>
#include <Audioclient.h>
#include <Setupapi.h>
#include "..\..\..\GfxValSimulator\GfxValSimLibrary\GfxValSim.h"
#include "WavePlayer.h"
#include "..\Logger\log.h"

#define MAX_STR_LEN 256
#define MAX_NUM_DEVICES 90
#define MAX_ENDPOINT_NAME_LENGTH 128
#define DEVICE_NAME_INTEL_AUDIO_CODEC L"Intel(R) Display Audio"
#define DEVICE_NAME_ACX_AUDIO_CODEC L"HD Audio Driver for Display Audio"
#define DEVICE_NAME_MS_AUDIO_CODEC L"High Definition Audio"

typedef struct _AUDIO_ENDPOINT_NAME_INFO
{
    _Out_ UINT FormFactor;
    _Out_ WCHAR EndPointName[MAX_ENDPOINT_NAME_LENGTH];
} AUDIO_ENDPOINT_NAME_INFO, *PAUDIO_ENDPOINT_NAME_INFO;

typedef struct _AUDIO_ENDPOINT_NAME
{
    _Out_ INT Count;
    _Out_ AUDIO_ENDPOINT_NAME_INFO EndPointInfo[MAX_NUM_AUDIO_END_POINTS];
} AUDIO_ENDPOINT_NAME, *PAUDIO_ENDPOINT_NAME;

typedef struct _AUDIO_ENDPOINT_COUNT
{
    _Out_ INT Count;
} AUDIO_ENDPOINT_COUNT, *PAUDIO_ENDPOINT_COUNT;

typedef enum _AUDIO_CODEC_TYPE
{
    INTEL_AUDIO_CODEC = 1,
    ACX_AUDIO_CODEC   = 3
} AUDIO_CODEC_TYPE;

typedef enum _AUDIO_CONTROLLER_TYPE
{
    INTEL_AUDIO_CONTROLLER = 1,
    MS_AUDIO_CONTROLLER    = 2
} AUDIO_CONTROLLER_TYPE;

class NotificationClient : public IMMNotificationClient
{
    IMMDeviceEnumerator *pEnumerator = NULL;

    HRESULT _PrintDeviceName(LPCWSTR pwstrId)
    {
        HRESULT         hr      = S_OK;
        IMMDevice *     pDevice = NULL;
        IPropertyStore *pProps  = NULL;
        PROPVARIANT     varString;

        CoInitialize(NULL);
        PropVariantInit(&varString);

        if (pEnumerator == NULL)
        {
            return S_FALSE;
        }
        if (hr == S_OK)
        {
            hr = pEnumerator->GetDevice(pwstrId, &pDevice);
        }
        if (hr == S_OK)
        {
            hr = pDevice->OpenPropertyStore(STGM_READ, &pProps);
        }
        if (hr == S_OK)
        {
            // Get the endpoint device's friendly-name property.
            hr = pProps->GetValue(PKEY_Device_FriendlyName, &varString);
        }
        INFO_LOG("----------------------\nDevice name: \"%S\"\n"
                 "  Endpoint ID string: \"%S\"\n",
                 (hr == S_OK) ? varString.pwszVal : L"null device", (pwstrId != NULL) ? pwstrId : L"null ID");

        PropVariantClear(&varString);

        SAFE_RELEASE(pProps)
        SAFE_RELEASE(pDevice)
        CoUninitialize();
        return hr;
    };

  public:
    std::vector<wstring> activeEndpointList;

    NotificationClient(IMMDeviceEnumerator *DeviceEnumerator)
    {
        pEnumerator = DeviceEnumerator;
    }

    STDMETHODIMP_(ULONG) AddRef() override
    {
        return 1;
    }
    STDMETHODIMP_(ULONG) Release() override
    {
        return 1;
    }
    STDMETHODIMP QueryInterface(REFIID riid, void **ppv) override
    {
        if (riid == IID_IUnknown)
        {
            *ppv = static_cast<IMMNotificationClient *>(this);
            return S_OK;
        }
        *ppv = nullptr;
        return E_NOINTERFACE;
    }

    // The OnDeviceStateChanged method is called when the state of an audio device changes
    STDMETHODIMP OnDeviceStateChanged(LPCWSTR pwstrDeviceId, DWORD dwNewState) override
    {
        // INFO_LOG("AudioNotification Device Statechange ID: %-25S ", pwstrDeviceId);
        if (dwNewState & DEVICE_STATE_ACTIVE)
        {
            wstring deviceID(pwstrDeviceId);

            // Check if Endpoint is already there in List.
            bool isDuplicateEntry = false;
            for (std::vector<wstring>::iterator iter = activeEndpointList.begin(); iter != activeEndpointList.end(); ++iter)
            {
                if (*iter == deviceID)
                {
                    isDuplicateEntry = true;
                    break;
                }
            }
            if (isDuplicateEntry == false)
            {
                activeEndpointList.emplace_back(deviceID);
            }

            INFO_LOG("AudioNotification Device Active ID: %-25S ", pwstrDeviceId);
        }

        if (dwNewState & DEVICE_STATE_DISABLED)
        {
            INFO_LOG("AudioNotification Device Disabled ID: %-25S ", pwstrDeviceId);
        }

        if (dwNewState & DEVICE_STATE_NOTPRESENT)
        {
            wstring deviceID(pwstrDeviceId);
            for (std::vector<wstring>::iterator iter = activeEndpointList.begin(); iter != activeEndpointList.end(); ++iter)
            {
                if (*iter == deviceID)
                {
                    activeEndpointList.erase(iter);
                    break;
                }
            }

            INFO_LOG("AudioNotification Device NotPresent ID: %-25S ", pwstrDeviceId);
        }

        if (dwNewState & DEVICE_STATE_UNPLUGGED)
        {
            INFO_LOG("AudioNotification Device Unplugged ID: %-25S ", pwstrDeviceId);
        }
        _PrintDeviceName(pwstrDeviceId);
        return S_OK;
    }

    // The OnDeviceAdded method is called when a new audio device is added
    STDMETHODIMP OnDeviceAdded(LPCWSTR pwstrDeviceId) override
    {
        INFO_LOG("AudioNotification Device added ID: %-25S ", pwstrDeviceId);
        _PrintDeviceName(pwstrDeviceId);
        return S_OK;
    }

    // The OnDeviceRemoved method is called when an audio device is removed
    STDMETHODIMP OnDeviceRemoved(LPCWSTR pwstrDeviceId) override
    {
        INFO_LOG("AudioNotification Device removed ID: %-25S ", pwstrDeviceId);
        return S_OK;
    }

    // The OnDefaultDeviceChanged method is called when the default audio device changes
    STDMETHODIMP OnDefaultDeviceChanged(EDataFlow flow, ERole role, LPCWSTR pwstrDefaultDeviceId) override
    {
        INFO_LOG("AudioNotification default device changed ID: %-25S ", pwstrDefaultDeviceId);
        return S_OK;
    }

    // The OnPropertyValueChanged method is called when a property value of an audio device changes
    STDMETHODIMP OnPropertyValueChanged(LPCWSTR pwstrDeviceId, const PROPERTYKEY key) override
    {
        INFO_LOG("AudioNotification Property values changed  ID: %-25S ", pwstrDeviceId);
        return S_OK;
    }
};

DLLEXPORT int dllversion();

DLLEXPORT HRESULT PlayAudioAndVerify(const CHAR *waveFileToPlay, const CHAR *EndPointName, const CHAR *portType, PGFX_ADAPTER_INFO pAdapterInfo);

DLLEXPORT HRESULT PlayAudio(const CHAR *waveFileToPlay, const CHAR *EndPointName, const CHAR *portType);

DLLEXPORT HRESULT GetAudioEndpointNames(PAUDIO_ENDPOINT_NAME pEndpointInfo);

DLLEXPORT DEVICE_POWER_STATE GetAudioCodecPowerState(int audio_codec_type, PWCHAR codec_name);

DLLEXPORT BOOL GetAudioControllerPowerState(PWCHAR controller_name);

DLLEXPORT HRESULT CreateEnumerator();

DLLEXPORT HRESULT CreateAndRegisterNotificationClient();

DLLEXPORT void DestroyEnumerator();