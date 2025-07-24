// Dlg_CBLV.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CBLV.h"
#include "stdlib.h"


// CDlg_CBLV dialog

IMPLEMENT_DYNAMIC(CDlg_CBLV, CDialog)

CDlg_CBLV::CDlg_CBLV(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CBLV::IDD, pParent)
    , m_CBLVValue(_T(""))
{

}

CDlg_CBLV::~CDlg_CBLV()
{
}

void CDlg_CBLV::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    ULONG ulValid = m_ACPIMailboxManager.stBiosDriverMailbox.ulCurrentBrightness.FieldValidBit;
    ULONG ulCBLVValue = m_ACPIMailboxManager.stBiosDriverMailbox.ulCurrentBrightness.BackLightBrightness;
    char str[100];
    
    if(ulValid)
    {
        _ultoa(ulCBLVValue, str, 10);
        m_CBLVValue = (CString) str;
    }
    else
        m_CBLVValue = L"Invalid Data";

    UpdateData(FALSE);
}


void CDlg_CBLV::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_CBString(pDX, IDC_COMBO_CBLV, m_CBLVValue);
}


BEGIN_MESSAGE_MAP(CDlg_CBLV, CDialog)
END_MESSAGE_MAP()


// CDlg_CBLV message handlers
