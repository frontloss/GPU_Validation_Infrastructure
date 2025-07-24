#include "StdAfx.h"

#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"


#ifndef NTSTATUS
#define NTSTATUS int
#endif
#include "inc\d3dkmthk.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif



ACPIMbxManager::ACPIMbxManager(void)
{
    ZeroMemory(&stACPIMbx, 0x100);
    ZeroMemory(&stBiosDriverMailbox, 0x100);
}

ACPIMbxManager::~ACPIMbxManager(void)
{
    bMailboxValid = false;
    ulMbxSize = 0;
    

}

bool ACPIMbxManager::GetMailboxData(void)
{
    void *pInputBuffer = NULL;
    void *pOutputBuffer = NULL;
    void *pTempBuffer = NULL;

    ULONG ulInputBufferSize = 0;
    ULONG ulOutputBufferSize = 0;
    ULONG ulStatus = 0 ;

    bMailboxValid = false;   
    ulOutputBufferSize = 0x200;
    pOutputBuffer = malloc(ulOutputBufferSize);


    //Get Mailbox #1
    esc.DoACPIEsc(
        GFX_ESC_ACPI_SIGNATURE_CODE, 
        ESC_ACPI_READ_MBX,
        GFX_ESCAPE_ACPI_CONTROL,
        &pInputBuffer,
        &pOutputBuffer,
        ulInputBufferSize,
        0x100,
        &ulStatus);

    pTempBuffer = (char *)pOutputBuffer + sizeof(ACPI_MBX);

    //Get Mailbox #3
    esc.DoACPIEsc(
        GFX_ESC_ACPI_SIGNATURE_CODE, 
        ESC_ACPI_READ_BIOS_DRV_MBX,
        GFX_ESCAPE_ACPI_CONTROL,
        &pInputBuffer,
        &pTempBuffer,
        ulInputBufferSize,
        0x100,
        &ulStatus);

    //Copy mailboxes
    memcpy(&stACPIMbx, pOutputBuffer, sizeof(ACPI_MBX));

    memcpy(&stBiosDriverMailbox, (char *)pOutputBuffer + sizeof(ACPI_MBX), sizeof(BIOSDRIV_MBX));

    ulMbxSize = sizeof(ACPI_MBX) + sizeof(BIOSDRIV_MBX);


    bMailboxValid = true;

    if(pOutputBuffer)
    {
        free(pOutputBuffer);
        pOutputBuffer = NULL;
    }

    return true;
}

