/**
 * @file		PowerConsEscapesTest.c
 * @brief	This file demonstrates how to use APIs exposed by PowerConsEscapes.dll
 *
 * @author	Ashish Tripathi
 */

#include "PowerConsEscapesTest.h"

/* Structures and variables to hold the fetched data*/
HMODULE hLib = NULL;

INT main()
{

    INT index = 0;
    /* Load and verify*/
    hLib = LoadDLL();
    if (NULL == hLib)
    {
        printf("\nFailed to Load DLL\n");
        return FALSE;
    }
    TestALSOverride(TRUE, 100);
    getchar();
}

/* Load PowerConsEscapes DLL*/
HMODULE LoadDLL()
{
    /* Load and get handle*/
    HMODULE retVal    = LoadLibraryA("..\\..\\..\\bin\\PowerConsEscapes.dll");
    DWORD   valReturn = GetLastError();
    return retVal;
}

/**
 * @brief									Driver Escape call for AlsOverride
 *											Set up data structure and send to driver
 * @param[in]	override					Boolean argument to override
 * @param[in]	lux							lux value
 * @return		VOID
 */
VOID TestALSOverride(BOOLEAN override, INT lux)
{
    HRESULT     errorCode = S_FALSE;
    BOOLEAN     status;
    INT_NO_ARGS alsOverride = (INT_NO_ARGS)GetProcAddress(hLib, "AlsOverride");
    status                  = (alsOverride)(override, lux, &errorCode);
    if (errorCode != S_OK)
    {
        printf("Error Code: %ld", errorCode);
    }
    printf("ALSOverride : %s", (status) ? "Success" : "Failed");
}
