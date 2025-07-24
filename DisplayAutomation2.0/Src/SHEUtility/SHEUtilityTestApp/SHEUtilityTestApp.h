/* System Include*/
#include <stdio.h>
#include <Windows.h>

/* User Include*/
#include "..\SHEUtility\SHEUtility.h"

/* Strutures and variables to hold the fetched data*/
HMODULE hLib      = NULL;
HRESULT errorCode = S_OK;

/* Exposed API function poinetrs of SystemUtility DLL*/
typedef HRESULT(__cdecl *SHEDevicePresent)();
typedef HRESULT(__cdecl *HotPlugUnPlug)(DISPLAYTYPE dType, int delay);
typedef HRESULT(__cdecl *eDPUnplugPLug)(DISPLAYTYPE dType, int delay1, int delay2);
typedef HRESULT(__cdecl *eDPUnplugPLugHibernateWake)(DISPLAYTYPE dType, int delay1, int delay2);
// typedef HRESULT(__cdecl *HotUnPlug1)(DISPLAYTYPE dType, int delay);
typedef HRESULT(__cdecl *PowerSwitch)(POWERLINE status, int delay);
typedef HRESULT(__cdecl *DockSwitch)(DOCKSWITCHSTATE status, int delay);
typedef HRESULT(__cdecl *ReservedPortSwitch)(RESERVEDSTATE status, int delay);
typedef HRESULT(__cdecl *LidSwitch)(LIDSWITCHSTATE status, int delay);

/* Helper functions*/
HMODULE     LoadDLL();
void        CheckLidSwitch(LIDSWITCHSTATE action);
void        PowerLineSwitch(POWERLINE val, int delay);
void        DockStatusSwitch(DOCKSWITCHSTATE val, int delay);
void        ReservedStatusSwitch(RESERVEDSTATE val, int delay);
bool        SHEDeviceAttached();
void        HotPlugDisplay(DISPLAYTYPE displayType, int delay);
void        HotUnPlugDisplay(DISPLAYTYPE displayType, int delay);
void        DispeDPUnplugPLug(DISPLAYTYPE displayType, int delay1, int delay2);
void        DispeDPUnplugPLugHibernateWake(DISPLAYTYPE displayType, int delay1, int delay2);
DISPLAYTYPE GetDisplayType(char *displayStr);
