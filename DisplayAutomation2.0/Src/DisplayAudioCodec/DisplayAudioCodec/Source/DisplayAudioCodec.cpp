#include "..\Header\DisplayAudioCodec.h"
#include "..\Header\Common.h"
#pragma warning(disable : 4996)

HRESULT PlayAudioAndVerify(const CHAR *waveFileToPlay, const CHAR *EndPointName, const CHAR *PortType, PGFX_ADAPTER_INFO pAdapterInfo)
{
    INFO_LOG("Verify Audio Playback: PortType: \"%s\" Endpoint: \"%s\" AudioFile: %s", PortType, EndPointName, waveFileToPlay);

    BOOL      bListen = FALSE;
    BOOL      bVerify = TRUE;
    HRESULT   hr      = E_FAIL;
    WCHAR     WCwaveFileToPlay[256];
    WCHAR     devName[32];
    PORT_TYPE EnumPortType = PORT_TYPE_MAX;

    size_t cSize = strlen(waveFileToPlay) + 1;
    mbstowcs(WCwaveFileToPlay, waveFileToPlay, cSize);

    cSize = strlen(EndPointName) + 1;
    mbstowcs(devName, EndPointName, cSize);

    if (0 == stricmp(PortType, "edp"))
    {
        EnumPortType = PORT_TYPE_EMBEDDED;
    }
    else if (0 == stricmp(PortType, "hdmi"))
    {
        EnumPortType = PORT_TYPE_HDMI;
    }
    else if (0 == stricmp(PortType, "dp"))
    {
        EnumPortType = PORT_TYPE_DP;
    }

    WavePlayer *pWavPlayer = NULL;
    pWavPlayer             = new WavePlayer(devName, EnumPortType, WCwaveFileToPlay, bListen, bVerify);
    hr                     = pWavPlayer->PlayWaveFile(pAdapterInfo);
    delete pWavPlayer;

    INFO_LOG("Audio Playback Verification Completed for PortType: \"%s\" Endpoint: \"%s\" with Status: %l", PortType, EndPointName, hr);
    return hr;
}

HRESULT PlayAudio(const CHAR *waveFileToPlay, const CHAR *EndPointName, const CHAR *PortType)
{
    BOOL      bListen = FALSE;
    BOOL      bVerify = FALSE;
    HRESULT   hr      = E_FAIL;
    WCHAR     WCwaveFileToPlay[256];
    WCHAR     devName[32];
    PORT_TYPE EnumPortType = PORT_TYPE_MAX;

    size_t cSize = strlen(waveFileToPlay) + 1;
    mbstowcs(WCwaveFileToPlay, waveFileToPlay, cSize);

    cSize = strlen(EndPointName) + 1;
    mbstowcs(devName, EndPointName, cSize);

    if (0 == stricmp(PortType, "edp"))
    {
        EnumPortType = PORT_TYPE_EMBEDDED;
    }
    else if (0 == stricmp(PortType, "hdmi"))
    {
        EnumPortType = PORT_TYPE_HDMI;
    }
    else if (0 == stricmp(PortType, "dp"))
    {
        EnumPortType = PORT_TYPE_DP;
    }

    WavePlayer *pWavPlayer = NULL;
    pWavPlayer             = new WavePlayer(devName, EnumPortType, WCwaveFileToPlay, bListen, bVerify);
    hr                     = pWavPlayer->PlayWaveFile();

    delete pWavPlayer;

    return hr;
}

DEVICE_POWER_STATE GetDevicePowerState(CONST GUID *ClassGuid, PWCHAR deviceName)
{
    DEVICE_POWER_STATE powerState = PowerDeviceUnspecified;
    HDEVINFO           devInfo    = SetupDiGetClassDevs(ClassGuid, NULL, NULL, 0);
    BOOL               bResult;
    CM_POWER_DATA      powerData         = { 0 };
    SP_DEVINFO_DATA    deviceData        = { 0 };
    WCHAR              name[BUFFER_SIZE] = { 0 };

    deviceData.cbSize = sizeof(SP_DEVINFO_DATA);
    DWORD deviceIndex = 0;

    while (deviceIndex < MAX_NUM_DEVICES)
    {
        bResult = SetupDiEnumDeviceInfo(devInfo, deviceIndex, &deviceData);

        if (bResult)
        {
            bResult = SetupDiGetDeviceRegistryPropertyW(devInfo, &deviceData, SPDRP_DEVICEDESC, NULL, (PBYTE)name, sizeof(name), NULL);
        }

        if (bResult)
        {
            if (wcsstr(name, deviceName) != NULL)
            {
                bResult = SetupDiGetDeviceRegistryPropertyW(devInfo, &deviceData, SPDRP_DEVICE_POWER_DATA, NULL, (PBYTE)&powerData, sizeof(powerData), NULL);

                if (bResult)
                {
                    powerState = powerData.PD_MostRecentPowerState;
                }

                break;
            }
        }

        deviceIndex++;
    }
    return powerState;
}

DEVICE_POWER_STATE GetAudioCodecPowerState(int audio_codec_type, PWCHAR codec_name)
{
    CoInitialize(NULL);
    codec_name               = (audio_codec_type == ACX_AUDIO_CODEC ? PWCHAR(DEVICE_NAME_ACX_AUDIO_CODEC) : PWCHAR(DEVICE_NAME_INTEL_AUDIO_CODEC));
    DEVICE_POWER_STATE power = GetDevicePowerState(&MEDIA_GUID, codec_name);
    CoUninitialize();
    return power;
}

BOOL GetAudioControllerPowerState(PWCHAR controller_name)
{
    CoInitialize(NULL);
    BOOL status = FALSE;
    DEVICE_POWER_STATE powerState = GetDevicePowerState(&SYSTEM_DEVICE_GUID, controller_name);
    if (powerState == 4)
    {
        status = TRUE;
        return status;
    }
    else
    {
        return status;
    }
    CoUninitialize();
}

int dllversion()
{
    return DLLVERSION;
}