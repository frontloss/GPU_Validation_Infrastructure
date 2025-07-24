#pragma once

#include <Windows.h>
#include "d3dkmthk.h"
#include "../../../Logger/log.h"

#define GDI32_DLL L"gdi32.dll"

char LIBRARY_NAME[22] = "VBIEnable.exe";

typedef struct _D3DKMT_ARGS
{
    HMODULE                              gdi32handle;
    PFND3DKMT_WAITFORVERTICALBLANKEVENT2 pfnWaitForVerticalBlankEvent2;
    PFND3DKMT_OPENADAPTERFROMHDC         pfnOpenAdapterFromHDC;
    PFND3DKMT_CLOSEADAPTER               pfnCloseAdapter;
} D3DKMT_ARGS;

D3DKMT_ARGS D3DKMTGetHandle();
