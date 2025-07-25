// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"
#include "EscapeHandler.h"
extern EscapeHandler *hEscape;
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
					 )
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
        hEscape = EscapeHandler::AcquireEscapeHandler();
        break;
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
        break;
	case DLL_PROCESS_DETACH:
        EscapeHandler::ReleaseEscapeHandler(&hEscape);
		break;
	}
	return TRUE;
}

