#pragma once

#include "windows.h"
typedef LONG NTSTATUS;

#include "d3dkmthk.h"

#include "gfxEscape.h"


typedef struct _D3DKMT_INTERFACES_TMP
{
    PFND3DKMT_OPENADAPTERFROMGDIDISPLAYNAME    pfnOpenAdapterFromGDIDisplayName;
    PFND3DKMT_OPENADAPTERFROMDEVICENAME        pfnOpenAdapterFromDeviceName;
    PFND3DKMT_CLOSEADAPTER                     pfnCloseAdapter;
    PFND3DKMT_CREATEDEVICE                     pfnCreateDevice;
    PFND3DKMT_DESTROYDEVICE                    pfnDestroyDevice;
    PFND3DKMT_ESCAPE                           pfnEscape;

}D3DKMT_INTERFACES_TMP, *PD3DKMT_INTERFACES_TMP;

class EscapeHandler
{
private:
    D3DKMT_HANDLE               m_AdapterHandle;
    D3DKMT_HANDLE               m_DeviceHandle;
    D3DKMT_INTERFACES_TMP           m_D3dKmtInterfaces;
    HMODULE                     m_Gdi32Handle;
    EscapeHandler();
    ~EscapeHandler();
    UINT Checksum(UINT uiSize, PVOID pData);
public:

    static EscapeHandler* AcquireEscapeHandler();
    static HRESULT ReleaseEscapeHandler(EscapeHandler** pEscHandler);

    HRESULT Initialize();
    HRESULT PerformEscape(int escapecode, void *pInputData, UINT  uiInputSize, BOOL  bNeedHWAccess, BOOL bIsInit = FALSE);
    HRESULT PerformEscape(GFX_ESCAPE_HEADER_T *pInputData, UINT  uiInputSize, BOOL  bNeedHWAccess, BOOL bIsInit = FALSE);
};


