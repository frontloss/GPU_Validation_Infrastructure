// Dlg_BCLP.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_BCLP.h"
#include "stdlib.h"


// Dlg_BCLP dialog

IMPLEMENT_DYNAMIC(Dlg_BCLP, CDialog)

Dlg_BCLP::Dlg_BCLP(CWnd* pParent /*=NULL*/)
	: CDialog(Dlg_BCLP::IDD, pParent)
    , m_BCLPValue(_T(""))
{

}

Dlg_BCLP::~Dlg_BCLP()
{
}

void Dlg_BCLP::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    ULONG ulBCLPVal = m_ACPIMailboxManager.stBiosDriverMailbox.ulBacklightBrightness.BackLightBrightness;
    ULONG ulValid = m_ACPIMailboxManager.stBiosDriverMailbox.ulBacklightBrightness.ulValue;
    char str[100];
    
    if(ulValid)
    {
        //m_BCLPValue = 
        _ultoa(ulBCLPVal, str, 10);
        m_BCLPValue = (CString) str;
    }
    else
        m_BCLPValue = L"Invalid Data";
    UpdateData(FALSE);
}

void Dlg_BCLP::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_EDIT1, m_BCLPValue);
}


BEGIN_MESSAGE_MAP(Dlg_BCLP, CDialog)
END_MESSAGE_MAP()


// Dlg_BCLP message handlers
