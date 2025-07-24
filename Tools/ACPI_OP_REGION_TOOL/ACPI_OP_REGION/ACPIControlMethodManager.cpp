#include "StdAfx.h"

#include "OPREG_Escape.h"

#include "ACPIControlMethodManager.h"

ACPIControlMethodManager::ACPIControlMethodManager(void)
{
}

ACPIControlMethodManager::~ACPIControlMethodManager(void)
{
}

bool ACPIControlMethodManager::EvaluateControlMethod(
    ULONG ulCommand,
    ULONG ulInputBufSize,
    ULONG ulOutputBufSize,
    PVOID pInputBuffer,
    PVOID pOutputBuffer)
{

    ULONG ulStatus = 0 ; //unused
    HRESULT hRes;

    //Evaluate Control Method
    hRes = esc.DoACPIEsc(
        GFX_ESC_ACPI_SIGNATURE_CODE, 
        (GFX_ESCAPE_ACPI_CONTROL_ACTION_T)ulCommand,
        GFX_ESCAPE_ACPI_CONTROL,
        &pInputBuffer,
        &pOutputBuffer,
        ulInputBufSize,
        ulOutputBufSize,
        &ulStatus);

    if(hRes != ERROR_SUCCESS)
        return false;
    else
        return true;
}
