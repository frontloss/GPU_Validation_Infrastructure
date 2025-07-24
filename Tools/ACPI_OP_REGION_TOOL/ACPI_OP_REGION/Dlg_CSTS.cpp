// Dlg_CSTS.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CSTS.h"
#include "stdlib.h"


// CDlg_CSTS dialog

IMPLEMENT_DYNAMIC(CDlg_CSTS, CDialog)

CDlg_CSTS::CDlg_CSTS(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CSTS::IDD, pParent)
{

}

CDlg_CSTS::~CDlg_CSTS()
{
}

void CDlg_CSTS::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCSTS = 0;
    ulCSTS = m_ACPIMailboxManager.stACPIMbx.ulNotificationStatus;
    
    m_CSTSCombo.ResetContent();

    m_CSTSCombo.AddString(L"Success (0)");
    m_CSTSCombo.SetItemData(0,0);

    m_CSTSCombo.AddString(L"Failure (1)");
    m_CSTSCombo.SetItemData(1,1);

    m_CSTSCombo.AddString(L"Pending (2)");
    m_CSTSCombo.SetItemData(2,2);

    m_CSTSCombo.AddString(L"Dispatched(3)");
    m_CSTSCombo.SetItemData(3,3);

    if((ulCSTS >=0 && ulCSTS <= 3))
    {
        m_CSTSCombo.SetCurSel(ulCSTS);
    }
    else
    {
        m_CSTSCombo.AddString(L"Invalid Data");
        m_CSTSCombo.SetItemData(4,4);
        m_CSTSCombo.SetCurSel(4);
    }

    UpdateData(FALSE);

}

void CDlg_CSTS::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_CSTS, m_CSTSCombo);
}


BEGIN_MESSAGE_MAP(CDlg_CSTS, CDialog)
END_MESSAGE_MAP()


// CDlg_CSTS message handlers
