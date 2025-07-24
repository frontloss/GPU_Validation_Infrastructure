#include <stdio.h>
#include <initguid.h>

#include "..\Header\DisplayAudioCodec.h";

char LIBRARY_NAME[22] = "DisplayAudioCodec.dll";

#define EXIT_ON_ERROR(hres) \
    if (FAILED(hres))       \
    {                       \
        goto Exit;          \
    }
#define SAFE_RELEASE(punk) \
    if ((punk) != NULL)    \
    {                      \
        (punk)->Release(); \
        (punk) = NULL;     \
    }
IMMDeviceEnumerator *pEnumerator         = NULL;
NotificationClient * pNotificationCLient = NULL;

HRESULT CreateEnumerator()
{
    HRESULT hr = S_OK;
    CoInitialize(nullptr);
    hr = CoCreateInstance(CLSID_MMDeviceEnumerator, NULL, CLSCTX_ALL, IID_IMMDeviceEnumerator, (void **)&pEnumerator);
    return hr;
}

void DestroyEnumerator()
{
    SAFE_RELEASE(pEnumerator);
}

HRESULT CreateAndRegisterNotificationClient()
{

    pNotificationCLient = new NotificationClient(pEnumerator);
    if (pEnumerator != NULL)
    {
        pEnumerator->RegisterEndpointNotificationCallback(pNotificationCLient);
        return S_OK;
    }
    else
    {
        ERROR_LOG("Error! pEnumerator is NULL");
        return S_FALSE;
    }
}

HRESULT GetAudioEndpointNames(PAUDIO_ENDPOINT_NAME pEndpointInfo)
{
    HRESULT              hr          = S_OK;
    IMMDeviceCollection *pCollection = NULL;
    IMMDevice *          pEndpoint   = NULL;
    IPropertyStore *     pProps      = NULL;
    LPWSTR               pwszID      = NULL;

    UINT count;
    if (pNotificationCLient == nullptr)
    {
        ERROR_LOG("Notification client is NULL");
        return E_FAIL;
    }

    count = pNotificationCLient->activeEndpointList.size();

    pEndpointInfo->Count = count;

    if (count == 0)
    {
        ERROR_LOG("No Audio Endpoints found");
    }

    // Each loop prints the name of an endpoint device.
    for (ULONG i = 0; i < count; i++)
    {
        wstring endpoint   = pNotificationCLient->activeEndpointList.at(i);
        LPCWSTR endpointID = endpoint.c_str();
        INFO_LOG("Get device for id %-25S", endpointID);
        hr = pEnumerator->GetDevice(endpointID, &pEndpoint);
        if (FAILED(hr))
            ERROR_LOG("Get device fail");
        EXIT_ON_ERROR(hr);

        hr = pEndpoint->OpenPropertyStore(STGM_READ, &pProps);
        if (FAILED(hr))
            ERROR_LOG("Open Store fail");
        EXIT_ON_ERROR(hr);

        PROPVARIANT endPointName;
        PROPVARIANT deviceType;
        PROPVARIANT portType;

        // Initialize container for property value.
        PropVariantInit(&endPointName);
        PropVariantInit(&deviceType);
        PropVariantInit(&portType);

        // Get the endpoint's Device Description property.
        hr = pProps->GetValue(PKEY_Device_DeviceDesc, &endPointName);
        if (FAILED(hr))
            ERROR_LOG("Get PKEY_Device_DeviceDesc fail");
        EXIT_ON_ERROR(hr);

        // Get the endpoint's device type property.
        hr = pProps->GetValue(PKEY_AudioEndpoint_FormFactor, &deviceType);
        if (FAILED(hr))
            ERROR_LOG("Get PKEY_AudioEndpoint_FormFactor fail");
        EXIT_ON_ERROR(hr);

        // Get Endpoint Port Type type
        hr = pProps->GetValue(PKEY_AudioEndpoint_JackSubType, &portType);
        if (FAILED(hr))
            ERROR_LOG("Get PKEY_AudioEndpoint_JackSubType fail");
        EXIT_ON_ERROR(hr);

        _GUID  guid;
        string sEndPointPortType = "UNKNOWN";

        hr = CLSIDFromString(portType.pwszVal, (LPCLSID)&guid);
        if (hr == S_OK)
        {
            if (IsEqualGUID(guid, KSNODETYPE_DISPLAYPORT_INTERFACE))
            {
                sEndPointPortType = "DP";
            }
            else if (IsEqualGUID(guid, KSNODETYPE_HDMI_INTERFACE))
            {
                sEndPointPortType = "HDMI";
            }
        }

        INFO_LOG("Endpoint %-2d: %-25S : [FormFactor:%2d] [PortType: %s]", i, endPointName.pwszVal, deviceType.uiVal, sEndPointPortType);

        pEndpointInfo->EndPointInfo[i].FormFactor = deviceType.uiVal;
        wcscpy_s(pEndpointInfo->EndPointInfo[i].EndPointName, wcslen(endPointName.pwszVal) + 1, endPointName.pwszVal);

        CoTaskMemFree(pwszID);
        pwszID = NULL;

        PropVariantClear(&endPointName);
        PropVariantClear(&deviceType);
        PropVariantClear(&portType);

        SAFE_RELEASE(pProps);
        SAFE_RELEASE(pEndpoint);
    }
    SAFE_RELEASE(pCollection);
    return hr;

Exit:
    ERROR_LOG("Error! Unable to get Audio Endpoint Name");
    CoTaskMemFree(pwszID);
    SAFE_RELEASE(pEnumerator);
    SAFE_RELEASE(pCollection);
    SAFE_RELEASE(pEndpoint);
    SAFE_RELEASE(pProps);
    return hr;
}