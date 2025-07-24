#include "StdAfx.h"


#ifndef NTSTATUS
#define NTSTATUS int
#endif

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

/*#ifndef ULONG	
#define ULONG unsigned long
#endif
#ifndef UINT
#define UINT unsigned int
#endif*/

#include "inc\d3dkmthk.h"
#include "..\\..\\..\\LHDM\inc\ACPICtrlDriverInterface.h"
#include <windows.h>
#include <windef.h>
#include <stdlib.h>
#include <stdio.h>
#include <conio.h>
#include <comdef.h>
#include "..\\..\\..\\LHDM\inc\AcpiCtrlEscape.h"

#include "OPREG_Escape.h"

OPREG_Escape::OPREG_Escape(void)
{
    
}

OPREG_Escape::~OPREG_Escape(void)
{

}

HRESULT OPREG_Escape::DoEsc(ULONG ulDataSize, 
                            void * pUserData, 
                            void * pError,
                            ULONG ulEscapeCode)
{
   HRESULT hr = E_FAIL;
   HDC hDC = NULL;
   ULONG ulRet = -1;

   GFX_ESCAPE_ACPI_INFO_BUFFER_T * pAcpiData = NULL;
   D3DKMT_OPENADAPTERFROMHDC* pOpenADapter = NULL;
   GFX_ESCAPE_HEADER_T *pHeader = NULL;
   D3DKMT_ESCAPE esc = {0};
   D3DKMT_CLOSEADAPTER *pCloseAdapter = NULL;
    
    do
    {

        //1. Getting Handle to Device Context
	    hDC=GetDC(NULL); 	
	    if(hDC==NULL)
	    {
		    printf("\n\t\tHandle to DC not created !!");
		    hr=E_UNEXPECTED;
		    break;
	    }

        SetLastError(0); 	//Setting Success till now

        //2. Open Adapter
        pOpenADapter = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
        ZeroMemory(pOpenADapter,sizeof(pOpenADapter));
        pOpenADapter->hDc = hDC;
        OpenAdapter(pOpenADapter);

        //3.Prepare Header
        pHeader = (GFX_ESCAPE_HEADER_T *)malloc(sizeof(GFX_ESCAPE_HEADER_T));
        if(NULL == pHeader)
        {
            hr = E_OUTOFMEMORY;
            //break;
        }

        ZeroMemory((void *)(pHeader),sizeof(GFX_ESCAPE_HEADER_T));
        pHeader->EscapeCode =  (GFX_ESCAPE_CODE_T)ulEscapeCode; 
        pHeader->Size = ulDataSize;
        //Calculation of checksum value of buffer data for the header
        //(*pHeader)->CheckSum = checksumLocal(iDataSize,(PVOID)(pUserData));
        //TODO: Add checksum
        pHeader->CheckSum = 0;

        //4. Prepare Escape Structure
        esc.hAdapter = pOpenADapter->hAdapter;
        esc.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
        esc.pPrivateDriverData = (void*)malloc(ulDataSize+sizeof(GFX_ESCAPE_HEADER_T));
        esc.PrivateDriverDataSize = ulDataSize+sizeof(GFX_ESCAPE_HEADER_T);

        ZeroMemory((void *)(esc.pPrivateDriverData),ulDataSize+sizeof(GFX_ESCAPE_HEADER_T));
        memcpy(esc.pPrivateDriverData,pHeader,sizeof(GFX_ESCAPE_HEADER_T));
        memcpy((char*)esc.pPrivateDriverData+sizeof(GFX_ESCAPE_HEADER_T),pUserData,ulDataSize);

        //5. Call Escape Interface
        ulRet = D3DKmtEscape(&esc);
        if(ulRet == 0)
            ulRet = 1;

        //6. Prepare Output Buffer
        if(ulRet > 0)
        {
            hr = S_OK;
            pAcpiData = (GFX_ESCAPE_ACPI_INFO_BUFFER_T *)pUserData;
            memcpy((char*)pUserData + sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T) + pAcpiData->ulACPIInputSize,
                    (char*)(esc.pPrivateDriverData) + sizeof(GFX_ESCAPE_HEADER_T) + pAcpiData->ulACPIInputSize + sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T),
                    pAcpiData->ulACPIOutputSize);

            pAcpiData->eEscACPIStatus=( (GFX_ESCAPE_ACPI_INFO_BUFFER_T *)((char*)(esc.pPrivateDriverData)+sizeof(GFX_ESCAPE_HEADER_T)) )->eEscACPIStatus;

        }

    }while(0);

    //7.  Close Adapter
    if(pOpenADapter)
    {
        pCloseAdapter = (D3DKMT_CLOSEADAPTER *)malloc(sizeof(D3DKMT_CLOSEADAPTER));
        pCloseAdapter->hAdapter = pOpenADapter->hAdapter;
        CloseAdapter(pCloseAdapter);
    }

    //8. Free memory
    if(pOpenADapter)
    {
        free(pOpenADapter);
        pOpenADapter = NULL;
    }

    if(esc.pPrivateDriverData)
    {
        free(esc.pPrivateDriverData);
        esc.pPrivateDriverData = NULL;
    }

    if(pHeader)
    {
        free(pHeader);
        pHeader = NULL;
    }

    if(pCloseAdapter)
    {
        free(pCloseAdapter);
        pCloseAdapter = NULL;
    }

    return hr;

}

HRESULT OPREG_Escape::DoACPIEsc(ULONG ulACPI_Signature,
                                GFX_ESCAPE_ACPI_CONTROL_ACTION_T gfxAction, 
                                ULONG ulEscapeCode, 
                                void ** ppUserInput, 
                                void ** ppUserOutput, 
                                ULONG ulInputSize, 
                                ULONG ulOutputSize,
                    
                                ULONG * pStatus)
{
        GFX_ESCAPE_ACPI_INFO_BUFFER_T * pGfxUserData = NULL;
        ULONG ulPacketSize = sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T)+ ulInputSize + ulOutputSize;
        ACPI_ERROR * pAcpiError = NULL;
		HRESULT hResult = E_FAIL;

        do
        {

            if(NULL == OpenAdapter)
                break;
            
            pGfxUserData=(GFX_ESCAPE_ACPI_INFO_BUFFER_T *)malloc(ulPacketSize);
            if(NULL == pGfxUserData)
            {
                hResult = E_OUTOFMEMORY;
                break;
            }

            //Fill subheader
            pGfxUserData->ulESC_ACPI_TOOL_VERSION= 0x10000;
            pGfxUserData->ulESC_ACPI_SIGNATURE_CODE=ulACPI_Signature;
            pGfxUserData->eEscACPIAction=gfxAction;
            pGfxUserData->eEscACPIStatus=ESC_ACPI_STATUS_FAILURE;

            //Fill body
            pGfxUserData->ulACPIInputSize = ulInputSize;
            pGfxUserData->ulACPIOutputSize = ulOutputSize;
            memcpy((char *)pGfxUserData + sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T), *ppUserInput, ulInputSize);
            //memcpy(pGfxUserData + sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T), *ppUserInput, ulInputSize);
            //memcpy(pGfxUserData + sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T) + ulInputSize , *ppUserOutput, ulOutputSize);


            //Initializing error code value, not being utilized currently
            pAcpiError=(ACPI_ERROR *)malloc(sizeof(ACPI_ERROR));
            if(NULL == pAcpiError)
            {
                hResult = E_OUTOFMEMORY;
                break;
            }

            ZeroMemory(pAcpiError, sizeof(ACPI_ERROR));
            pAcpiError->ErrorOccured=FALSE;
            pAcpiError->LastSystemErrorVal=GetLastError();
            pAcpiError->ExtendedError=ACPIERROR_MAX_ERROR;

            hResult = this->DoEsc(ulPacketSize, (void *) pGfxUserData, (void *) pAcpiError, ulEscapeCode);

            if(hResult!=S_OK)
            {
                pAcpiError->ErrorOccured=TRUE;
                pAcpiError->ExtendedError=ACPIERROR_UNEXPECTED;
                break;
            }
            
            memcpy((char *)(*ppUserOutput), (char *)pGfxUserData+sizeof(GFX_ESCAPE_ACPI_INFO_BUFFER_T)+pGfxUserData->ulACPIInputSize, pGfxUserData->ulACPIOutputSize);
            //memmove((void *)(pStatus), (void *)(pGfxUserData->eEscACPIStatus), sizeof(GFX_ESCAPE_ACPI_STATUS_T));

        }while(0);

        if(pGfxUserData)
        {
            free(pGfxUserData);
            pGfxUserData = NULL;
        }

        if(pAcpiError)
        {
            free(pAcpiError);
            pAcpiError = NULL;
        }
            


        return hResult;        
}