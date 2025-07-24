#pragma once
#include <Windows.h>
#include <vector>
#include "dxgi.h"
#include "GfxRegisterInfo.h"
#include "..\Header\DisplayAudioCodec.h"
#include "GfxValSim.h"
#include "..\Logger\log.h"

using namespace std;

#define IN _In_
#define OUT _Out_
#define IN_OUT _Inout_
#define RESERVED _Reserved_
#define IN_OUT_OPT _Inout_opt_

#define INTEL_VENDOR_ID 0x8086

#define DIVA_IOCTL_DEVICE_TYPE (0x8086)                           // Device type to be used for IOCTL calls; any value > 0x8000
#define DIVA_IOCTL_FUNC_CODE_BASE (0x808)                         // Base function code for IOCTL calls; any value > 0x800
#define DIVA_IOCTL_ACCESS_TYPE (FILE_READ_DATA | FILE_WRITE_DATA) // Type of access to be requested while opening the file object for device
#define _DIVA_CTL_CODE(_FxnCode) CTL_CODE(DIVA_IOCTL_DEVICE_TYPE, DIVA_IOCTL_FUNC_CODE_BASE + _FxnCode, METHOD_BUFFERED, DIVA_IOCTL_ACCESS_TYPE)
#define DIVA_DOS_DEVICE_NAME "\\\\.\\DivaKmd" // Symbolic DOS Name for the Device
#define DIVA_IOCTL_GfxValStubCommunication _DIVA_CTL_CODE(1)
#define GVSTUB_FEATURE_INFO_VERSION 0x1
#define GVSTUB_FEATURE_FAILURE 0x00000008
#define GVSTUB_FEATURE_SUCCESS 0x00000000

#define MINORESCAPEVERSION 1
#define MAJORESCAPECODE 20
#define PRODUCTIONESCAPEVERSION 0
#define DDRWESCAPEVERSION 1
#define ESCAPE_DISPLAY_CONTROL 1
#define INVALID_HANDLE_VALUE ((HANDLE)(LONG_PTR)-1)

#define SIM_IOCTL_DEVTYPE 0x9000
#define SIM_IOCTL_BASEVAL 0x801
#define SIM_IOCTL_COMMON 51
#define SIM_FILE_ACCESS (FILE_READ_ACCESS | FILE_WRITE_ACCESS)
#define IOCTL_SIMDRVTOGFX_MMIO_ACCESS CTL_CODE(SIM_IOCTL_DEVTYPE, (SIM_IOCTL_BASEVAL + SIM_IOCTL_COMMON + 7), METHOD_BUFFERED, SIM_FILE_ACCESS)
#define MAX_GFX_ADAPTER 5
#define GFX_0_ADPTER_INDEX L"gfx_0" // MA WA

#define VERIFY_STATUS(statusCode)                    \
    {                                                \
        if (0 != statusCode)                         \
            INFO_LOG("StatusCode : %d", statusCode); \
    }

typedef union _DAC_VERB {
    ULONG ulValue;
    union {
        struct
        {
            unsigned int PayloadData : 8; // bit[7:0]
            unsigned int VerbId : 12;     // bit[19:8]
            unsigned int WidgetId : 8;    // bit[27:20]
            unsigned int CADValue : 4;    // bit[28:31]
        } verbLong;

        struct
        {
            unsigned int PayloadData : 16; // bit[15:0]
            unsigned int VerbId : 4;       // bit[19:16]
            unsigned int WidgetId : 8;     // bit[27:20]
            unsigned int CADValue : 4;     // bit[28:31]
        } verbShort;

        DWORD raw;
    };
} DAC_VERB;

class GFXMMIO
{
  public:
    GFXMMIO(PGFX_ADAPTER_INFO pAdapterInfoObj);
    ~GFXMMIO();
    HRESULT           MMIOWrite(ULONG offset, ULONG regValue);
    HRESULT           MMIORead(ULONG offset, ULONG *pRegValue);
    HRESULT           GetSetAudioVerb(ULONG ulWidgetId, ULONG ulVerbId, ULONG ulPayload, ULONG *pReadVal);
    PGFX_ADAPTER_INFO pAdapterInfo = NULL;

  private:
    HRESULT GetSetAudioVerbRaw(ULONG verb, ULONG *pReadVal);
    HRESULT SetMMIOPIOMode(BOOLEAN bSet);
    LUID    mAdapterLuid;
    DWORD   AdapterNo;
    bool    bDiva   = true;
    bool    bValsim = true;
};
