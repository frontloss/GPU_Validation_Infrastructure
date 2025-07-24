// Dlg_ALSI.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_ALSI.h"
#include "stdlib.h"


// CDlg_ALSI dialog

IMPLEMENT_DYNAMIC(CDlg_ALSI, CDialog)

CDlg_ALSI::CDlg_ALSI(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_ALSI::IDD, pParent)
    , m_ALSValue(0)
{

}

CDlg_ALSI::~CDlg_ALSI()
{
}

void CDlg_ALSI::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    ULONG ulALSVal = m_ACPIMailboxManager.stBiosDriverMailbox.ulALSReading.ALSData;
    m_ALSValue = ulALSVal;   
    UpdateData(FALSE);
}


void CDlg_ALSI::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_EDIT1, m_ALSValue);
}


BEGIN_MESSAGE_MAP(CDlg_ALSI, CDialog)
END_MESSAGE_MAP()


// CDlg_ALSI message handlers
