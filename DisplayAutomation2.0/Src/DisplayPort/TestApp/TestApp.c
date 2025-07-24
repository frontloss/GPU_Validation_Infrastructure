#include "stdafx.h"
#include <windows.h>
#include "..\DisplayPortUtility.h"

typedef HRESULT(__cdecl *DLLDivaKMDConn)();
typedef HRESULT(__cdecl *GetDPAPIVersion)(PINT pVersion);

// Function prototypes
void VerifyDLLDIVAConnection(HMODULE handle);
void GetDPInterfaceVersion(HMODULE handle);

/*
 * @brief        Sample App which gets DisplayPort utility handle & calls functions exported by it
 * @param[In]    Zero
 * @return       INT
 */
int _tmain(int argc, _TCHAR *argv[])
{
    printf("\n**********************************************************************************\n");
    printf("Sample App which gets DisplayPort utility handle & calls functions exported by it.");
    printf("\n**********************************************************************************\n");

    // Load DisplayPort.dll library
    HMODULE handle = LoadLibraryA("C:\\Automation\\DisplayPort\\x64\\Debug\\DisplayPort.dll");

    if (NULL != handle)
    {
        printf("DLL DisplayPort.dll loaded Successfully.\n");

        // Verify DLL to DIVA KMD connection status
        VerifyDLLDIVAConnection(handle);

        // Get DisplayPort DLL interface version
        GetDPInterfaceVersion(handle);

        FreeLibrary(handle);
    }
    else
    {
        printf("DLL load failed!\n");
    }
    return 0;
}

/*
 * @brief        VerifyDLLDIVAConnection function gets handle to DisplayPort.DLL and calls few functions
 *               exported by it to verify connection b/w DLL and DIVA KMD
 * @param[In]    Handle of DIVA KMD driver
 * @return       VOID
 */
void VerifyDLLDIVAConnection(HMODULE handle)
{
    // Get the address of function DLLDivaKMDConnection
    DLLDivaKMDConn VerifyDLLDivaKMDConnStatus = (DLLDivaKMDConn)GetProcAddress(handle, "Get_DLLToDivaKMDConnectionStatus");

    // Verify DLL to DIVA KMD connection status
    VerifyDLLDivaKMDConnStatus();
}

/*
 * @brief        GetDPInterfaceVersion function gets DisplayPort DLL's Interface version
 * @param[In]    Handle to DIVA KMD driver
 * @return       VOID
 */
void GetDPInterfaceVersion(HMODULE handle)
{
    INT Version = 0x0;

    // Get the address of function DLLDivaKMDConnection
    GetDPAPIVersion GetDisplayPortAPIVersion = (GetDPAPIVersion)GetProcAddress(handle, "Get_DisplayPortInterfaceVersion");

    // Get DisplayPort DLL interface version
    GetDisplayPortAPIVersion(&Version);

    printf("DisplayPort API Version: %d\n", Version);
}