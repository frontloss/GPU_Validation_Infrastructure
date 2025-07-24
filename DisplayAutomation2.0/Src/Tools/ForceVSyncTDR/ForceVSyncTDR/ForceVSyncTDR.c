/**
 * @file
 * @addtogroup Tools_ForceVSyncTDR
 * @brief It generates TDR using VSync way.
 * Usage: ForceVSyncTDR.exe<br> Returns -1 if it fails, otherwise 0.
 * @author Suraj Gaikwad
 */

/* System Includes */
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include "winerror.h"
#include "Winbase.h"
#include "ForceVSyncTDR.h"
#include "CommonDetails.h"
#include <time.h>

HRESULT  errorCode  = S_OK;
HRESULT *pErrCode   = &errorCode;
BOOL     isForceTDR = FALSE;

/**
 * @brief Function to generate VSync TDR
 *
 * Function to generate VSync TDR using Driver Escape
 *
 * @param[in]	*pErrorCode Pointer to the variable HRESULT to check the result of the Escape Call
 * @return		VOID
 */
void TDRDriverEscape(HRESULT *pErrorCode)
{
    /* Check for the error parameter if it is passed properly or not,
    this check is done only for exported functions*/
    if (NULL == pErrorCode)
        return;

    *pErrorCode = S_OK;

    /*Initailise and get the OS escape handles*/
    HMODULE                      hGdi32       = NULL;
    PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter  = NULL;
    PFND3DKMT_ESCAPE             D3DKmtEscape = NULL;
    PFND3DKMT_CLOSEADAPTER       CloseAdapter = NULL;

    /* Load gdi32 library and proccess address for D3D KMT functions*/
    hGdi32 = LoadLibraryEx(L"gdi32.dll", NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
    if (hGdi32)
    {
        /* Get process handles to operate on for escape call*/
        OpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32, "D3DKMTOpenAdapterFromHdc");
        NULLPTRCHECK(OpenAdapter, *pErrorCode);
        D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32, "D3DKMTEscape");
        NULLPTRCHECK(D3DKmtEscape, *pErrorCode);
        CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32, "D3DKMTCloseAdapter");
        NULLPTRCHECK(CloseAdapter, *pErrorCode);
    }
    else
        NULLPTRCHECK(hGdi32, *pErrorCode);

    /* Enumerate through available displays as DISPLAY1 may not be always primary display*/
    DISPLAY_DEVICE deviceName;
    deviceName.cb = sizeof(DISPLAY_DEVICE);
    UINT16 devID  = 0;
    HDC    hdc    = NULL;

    while (EnumDisplayDevices(NULL, devID++, &deviceName, 0))
    {
        hdc = CreateDC(deviceName.DeviceName, NULL, NULL, 0);
        DEBUGPRINT("\n DeviceName: %S, DeviceString: %S \n", deviceName.DeviceName, deviceName.DeviceString);

        /* Check if Device context is valid not*/
        if (0 != hdc)
            break;
    }

    /* Using device context make a call to OpenAdapter*/
    D3DKMT_OPENADAPTERFROMHDC *pOpenAdapter = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
    NULLPTRCHECK(pOpenAdapter, *pErrorCode);

    ZeroMemory(pOpenAdapter, sizeof(pOpenAdapter));
    pOpenAdapter->hDc = hdc;

    /* creates a graphics adapter object*/
    if (OpenAdapter(pOpenAdapter) != S_OK)
    {
        *pErrorCode = E_OUTOFMEMORY;
        free(pOpenAdapter);
        return;
    }

    /* Prepare Escape header*/
    D3DKMT_ESCAPE esc = { 0 };
    ZeroMemory(&esc, sizeof(esc));
    esc.hAdapter           = pOpenAdapter->hAdapter;
    esc.Type               = D3DKMT_ESCAPE_TDRDBGCTRL;
    esc.pPrivateDriverData = (void *)malloc(sizeof(D3DKMT_ESCAPE_TDRDBGCTRL));
    NULLPTRCHECK(esc.pPrivateDriverData, *pErrorCode);

    esc.PrivateDriverDataSize = sizeof(D3DKMT_ESCAPE_TDRDBGCTRL);
    if (isForceTDR == TRUE)
    {
        (*(int *)esc.pPrivateDriverData) = D3DKMT_TDRDBGCTRLTYPE_FORCETDR;
    }
    else
    {
        (*(int *)esc.pPrivateDriverData) = D3DKMT_TDRDBGCTRLTYPE_VSYNCTDR;
    }

    /* Make a driver scape call*/
    ULONG ntret = D3DKmtEscape(&esc);
    CHECKERR(ntret, *pErrorCode);

    /* Release all memory*/
    D3DKMT_CLOSEADAPTER ca;
    ca.hAdapter = pOpenAdapter->hAdapter;
    CloseAdapter(&ca);

    /* Free all the mallocs*/
    free(pOpenAdapter);
    pOpenAdapter = NULL;

    free(esc.pPrivateDriverData);
    esc.pPrivateDriverData = NULL;

    /* Release handles and heap variables*/
    DeleteDC(hdc);
}

/* Main entry point*/
int main(int argc, char **argv)
{
    HKEY            hKey;
    HANDLE          h;
    DWORD           dwNumRecords;
    DWORD           tdrEventID = 4101, currentEventID;
    DWORD           dwBytesRead, dwBytesNeeded, dwReadFlags;
    DWORD           dwOldestRecordIndex, dwNewestRecordIndex;
    BYTE            bBuffer[1024];
    EVENTLOGRECORD *pRecord = (EVENTLOGRECORD *)bBuffer;
    BOOL            flag    = FALSE;

    if (argc > 0)
    {
        isForceTDR = TRUE;
    }
    h = OpenEventLog(NULL, TEXT("System"));
    /* Open the System event log and Clear it*/
    if (h)
    {
        if (ClearEventLog(h, NULL) == FALSE)
        {
            DEBUGPRINT("\n\n Error in Clearing the System Events Log ");
            return (-1);
        }
        CloseEventLog(h);
    }

    /*
    To enable Timeout Detection and Recovery (TDR) functionality, the TdrTestMode = TdrTestMode DWORD registry value,
    which is stored in the HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers key, must be set to 1.
    */

    /* Open the required Registry */
    long result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, TEXT("SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers"), 0, KEY_ALL_ACCESS, &hKey);

    if (result != 0)
    {
        DEBUGPRINT("\n\nError Occured ! Windows Error Code : %ld\n", result);
        return (-1);
    }

    DWORD value = 1;

    /* Write the value to the opened Registry Key*/
    RegSetValueEx(hKey, TEXT("TdrTestMode"), 0, REG_DWORD, (const BYTE *)&value, sizeof(value));
    RegCloseKey(hKey);

    /* Call to the TDRDriverEscape Function*/
    TDRDriverEscape(pErrCode);

    /* Sleep for 10 seconds for TDR to happen and logging of events*/
    Sleep(10000);
    h = OpenEventLog(NULL, TEXT("System"));
    /* Reading Windows System Event Log to Verify if TDR happened or not*/
    if (h)
    {
        GetNumberOfEventLogRecords(h, &dwNumRecords);
        DEBUGPRINT("Total Number of New Event Log Entries present : %lu ", dwNumRecords);

        GetOldestEventLogRecord(h, &dwOldestRecordIndex);
        dwNewestRecordIndex = (dwNumRecords + dwOldestRecordIndex) - 1;
        dwReadFlags         = EVENTLOG_BACKWARDS_READ | EVENTLOG_SEEK_READ;

        /* Read all the System Event Log Entries*/
        while (dwNumRecords != 0)
        {
            if (ReadEventLog(h, dwReadFlags, dwNewestRecordIndex, &bBuffer, sizeof(bBuffer), &dwBytesRead, &dwBytesNeeded) == TRUE)
            {
                /* Compare the Current Event ID with TDR's Event ID*/
                currentEventID = pRecord->EventID & 0x0000FFFF;
                if (currentEventID == tdrEventID)
                {
                    flag = TRUE;
                }
            }
            else
            {
                DEBUGPRINT("\nError in Reading the System Event Logs");
            }
            dwNewestRecordIndex--;
            dwNumRecords--;
        }
        CloseEventLog(h);
    }

    if (flag == TRUE)
    {
        DEBUGPRINT("\nVSync TDR was Successful\n");
        return 0;
    }
    else
    {
        DEBUGPRINT("\nVSync TDR was Unsuccessful\n");
        return -1;
    }
}