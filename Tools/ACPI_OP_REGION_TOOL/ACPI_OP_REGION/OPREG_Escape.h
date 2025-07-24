#pragma once

#include <comdef.h>
#include "..\\..\\..\\LHDM\inc\AcpiCtrlEscape.h"
#include "..\\..\\..\\LHDM\inc\gfxEscape.h"

class OPREG_Escape
{

/*private:
    static HMODULE hGdi32; //Handle to GDI Object
private:
    static PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter; //Open Adapter
private:
    static PFND3DKMT_ESCAPE D3DKmtEscape ; //Escape
private:
    static PFND3DKMT_CLOSEADAPTER CloseAdapter ; //Close Adapter
*/

public:
    OPREG_Escape(void);

public:
    ~OPREG_Escape(void);

public:
    HRESULT DoEsc(
        ULONG ulDataSize, 
        void * pUserData, 
        void *pError,
        ULONG ulEscapeCode);

public:
    HRESULT DoACPIEsc(
        ULONG ulACPI_Signature,
        GFX_ESCAPE_ACPI_CONTROL_ACTION_T gfxAction, 
        ULONG ulEscapeCode, 
        void** ppUserInput, 
        void** ppUserOutput, 
        ULONG ulInputSize, 
        ULONG ulOutputSize,
        ULONG * pStatus);
};
