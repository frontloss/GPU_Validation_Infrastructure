// Dlg_ARDY.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_ARDY.h"
#include "stdlib.h"


// CDlg_ARDY dialog

IMPLEMENT_DYNAMIC(CDlg_ARDY, CDialog)

CDlg_ARDY::CDlg_ARDY(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_ARDY::IDD, pParent)
{

}

CDlg_ARDY::~CDlg_ARDY()
{
}

void CDlg_ARDY::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char str[100];
    char *temp = NULL;
    ULONG ulARDY = 0;
    ulARDY = m_ACPIMailboxManager.stBiosDriverMailbox.ulDriverReadiness.ARDY;

    m_ARDY.ResetContent();

    m_ARDY.AddString(L"Driver is not ready (0)");
    m_ARDY.SetItemData(0,0);

    m_ARDY.AddString(L"Driver is ready (1)");
    m_ARDY.SetItemData(1,1);

    if((ulARDY >=0 && ulARDY <= 1))
    {
        m_ARDY.SetCurSel(ulARDY);
    }
    else
    {
        m_ARDY.AddString(L"Invalid Data");
        m_ARDY.SetItemData(2,2);
        m_ARDY.SetCurSel(2);
    }

    UpdateData(FALSE);

}

void CDlg_ARDY::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_ARDY, m_ARDY);
}


BEGIN_MESSAGE_MAP(CDlg_ARDY, CDialog)
END_MESSAGE_MAP()


// CDlg_ARDY message handlers
