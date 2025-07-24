#pragma once

#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <ctype.h>
#include <PowrProf.h>
#include <Cfg.h>
#include <Cfgmgr32.h>

#include <Mmdeviceapi.h>
#include <Audioclient.h>
#include <Setupapi.h>

#define MAX_NUM_AUDIO_END_POINTS 10
#define MAX_NUM_DEVICES 5
#define MAX_NUM_SADS 15
#define MAX_STR_LEN 256
#define MAX_NUM_PATHS 4

#define EXIT_ON_ERROR(hres) \
    if (S_OK != hr)         \
    {                       \
        goto Exit;          \
    }
#define CONTINUE_ON_ERROR(hres) \
    if (FAILED(hres))           \
    {                           \
        continue;               \
    }

#define SAFE_RELEASE(punk) \
    if ((punk) != NULL)    \
    {                      \
        (punk)->Release(); \
        (punk) = NULL;     \
    }

#define ERROR_MESSAGE "!!!! ERROR !!!! "
#define VERIFICATION_SUCCESS "!!!! VERIFICATION SUCCESS !!!! "
#define VERIFICATION_FAILURE "!!!! VERIFICATION FAILED !!!! "
#define VERIFICATION_OR_TEST_FAILURE "!!!! VERIFICATION OR TEST FAILURE !!!! "
#define WARNING_MESSAGE "!!!! WARNING !!!! "
#define SUCCESS_MESSAGE "**** SUCCESS ****"

#define ERROR_MESSAGE_W L"!!!! ERROR !!!! "
#define WARNING_MESSAGE_W L"!!!! WARNING !!!! "
#define SUCCESS_MESSAGE_W L"**** SUCCESS ****"

#define DEVICE_WORKING_MASK (DN_DRIVER_LOADED | DN_STARTED)
#define DEVICE_ISSUE_MASK (DN_HAS_PROBLEM | DN_MOVED | DN_PRIVATE_PROBLEM | DN_WILL_BE_REMOVED | DN_NEED_TO_ENUM)

// REFERENCE_TIME time units per second and per millisecond
#define REFTIMES_PER_SEC 10000000
#define REFTIMES_PER_MILLISEC 10000

#define NODETYPE_HDMI_INTERFACE L"{D1B9CC2A-F519-417f-91C9-55FA65481001}"
#define NODETYPE_DISPLAYPORT_INTERFACE L"{E47E4031-3EA6-418d-8F9B-B73843CCBA97}"
#define NODETYPE_SPEAKER L"{DFF21CE1-F70F-11D0-B917-00A0C9223196}"

typedef enum
{
    PORT_TYPE_HDMI     = 0,
    PORT_TYPE_DP       = 1,
    PORT_TYPE_EMBEDDED = 2,
    PORT_TYPE_ANALOG   = 3,
    PORT_TYPE_MAX      = 4
} PORT_TYPE;

DEFINE_GUIDSTRUCT("4d36e97d-e325-11ce-bfc1-08002be10318", SYSTEM_DEVICE_GUID_NAME);
#define SYSTEM_DEVICE_GUID DEFINE_GUIDNAMED(SYSTEM_DEVICE_GUID_NAME)

DEFINE_GUIDSTRUCT("4d36e96c-e325-11ce-bfc1-08002be10318", MEDIA_GUID_NAME);
#define MEDIA_GUID DEFINE_GUIDNAMED(MEDIA_GUID_NAME)

DEFINE_GUIDSTRUCT("4d36e968-e325-11ce-bfc1-08002be10318", DISPLAY_GUID_NAME);
#define DISPLAY_GUID DEFINE_GUIDNAMED(DISPLAY_GUID_NAME)

#ifdef DEFINE_PROPERTYKEY
#undef DEFINE_PROPERTYKEY
#define DEFINE_PROPERTYKEY(name, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8, pid) \
    EXTERN_C const PROPERTYKEY DECLSPEC_SELECTANY name = { { l, w1, w2, { b1, b2, b3, b4, b5, b6, b7, b8 } }, pid }
#endif

DEFINE_PROPERTYKEY(PKEY_AudioEndpoint_JackSubType, 0x1da5d803, 0xd492, 0x4edd, 0x8c, 0x23, 0xe0, 0xc0, 0xff, 0xee, 0x7f, 0x0e, 8);
DEFINE_PROPERTYKEY(PKEY_Device_FriendlyName, 0xa45c254e, 0xdf1c, 0x4efd, 0x80, 0x20, 0x67, 0xd1, 0x46, 0xa8, 0x50, 0xe0, 14);
DEFINE_PROPERTYKEY(PKEY_Device_DeviceDesc, 0xa45c254e, 0xdf1c, 0x4efd, 0x80, 0x20, 0x67, 0xd1, 0x46, 0xa8, 0x50, 0xe0, 2);
DEFINE_PROPERTYKEY(PKEY_AudioEndpoint_FormFactor, 0x1da5d803, 0xd492, 0x4edd, 0x8c, 0x23, 0xe0, 0xc0, 0xff, 0xee, 0x7f, 0x0e, 0);

#define NODETYPE_HDMI_INTERFACE L"{D1B9CC2A-F519-417f-91C9-55FA65481001}"
#define NODETYPE_DISPLAYPORT_INTERFACE L"{E47E4031-3EA6-418d-8F9B-B73843CCBA97}"
#define NODETYPE_SPEAKER L"{DFF21CE1-F70F-11D0-B917-00A0C9223196}"
