// IgfxExtBridge.cpp : Implementation of DLL Exports.


// Note: Proxy/Stub Information
//      To build a separate proxy/stub DLL, 
//      run nmake -f IgfxExtBridgeps.mk in the project directory.

#include "stdafx.h"
#include "resource.h"
#include <initguid.h>
#include "IgfxExtBridge.h"

#include "IgfxExtBridge_i.c"
#include "Display_Util_i.c"
#include "MCCS_Util_i.c"
#include "Power_Util_i.c"
#include "TV_Setting_i.c"
#include "D3D_Setting_i.c"
#include "SG_Util_i.c"

#include "DisplayUtil.h"
#include "MCCSUtil.h"
#include "PowerUtil.h"
#include "TVSetting.h"
#include "D3DSetting.h"
#include "SGUtil.h"

CComModule _Module;

BEGIN_OBJECT_MAP(ObjectMap)
OBJECT_ENTRY(CLSID_DisplayUtil, CDisplayUtil)
OBJECT_ENTRY(CLSID_MCCSUtil,	CMCCSUtil)
OBJECT_ENTRY(CLSID_PowerUtil,	CPowerUtil)
OBJECT_ENTRY(CLSID_TVSetting,	CTVSetting)
OBJECT_ENTRY(CLSID_D3DSetting,	CD3DSetting)
OBJECT_ENTRY(CLSID_SGUtil,	CSGUtil)
END_OBJECT_MAP()

/////////////////////////////////////////////////////////////////////////////
// DLL Entry Point

extern "C"
BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID /*lpReserved*/)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        _Module.Init(ObjectMap, hInstance, &LIBID_IGFXEXTBRIDGELib);
        DisableThreadLibraryCalls(hInstance);
    }
    else if (dwReason == DLL_PROCESS_DETACH)
        _Module.Term();
    return TRUE;    // ok
}

/////////////////////////////////////////////////////////////////////////////
// Used to determine whether the DLL can be unloaded by OLE

STDAPI DllCanUnloadNow(void)
{
    return (_Module.GetLockCount()==0) ? S_OK : S_FALSE;
}

/////////////////////////////////////////////////////////////////////////////
// Returns a class factory to create an object of the requested type

STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID* ppv)
{
    return _Module.GetClassObject(rclsid, riid, ppv);
}

/////////////////////////////////////////////////////////////////////////////
// DllRegisterServer - Adds entries to the system registry

STDAPI DllRegisterServer(void)
{
    // registers object, typelib and all interfaces in typelib
    return _Module.RegisterServer(TRUE);
}

/////////////////////////////////////////////////////////////////////////////
// DllUnregisterServer - Removes entries from the system registry

STDAPI DllUnregisterServer(void)
{
    return _Module.UnregisterServer(TRUE);
}


