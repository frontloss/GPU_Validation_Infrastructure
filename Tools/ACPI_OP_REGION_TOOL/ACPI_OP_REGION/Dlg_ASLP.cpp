// Dlg_ASLP.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_ASLP.h"
#include "stdlib.h"


// CDlg_ASLP dialog

IMPLEMENT_DYNAMIC(CDlg_ASLP, CDialog)

CDlg_ASLP::CDlg_ASLP(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_ASLP::IDD, pParent)
    , m_ASLPValue(0)
{

}

CDlg_ASLP::~CDlg_ASLP()
{
}

void CDlg_ASLP::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    ULONG ulASLSleepTimeOut = m_ACPIMailboxManager.stACPIMbx.ulASLSleepTimeOut;
    m_ASLPValue = ulASLSleepTimeOut;   
    UpdateData(FALSE);
}





void CDlg_ASLP::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_EDIT_ASLP, m_ASLPValue);
}


BEGIN_MESSAGE_MAP(CDlg_ASLP, CDialog)
END_MESSAGE_MAP()


// CDlg_ASLP message handlers
