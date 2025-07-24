// Dlg_CLID.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CLID.h"
#include "stdlib.h"


// CDlg_CLID dialog

IMPLEMENT_DYNAMIC(CDlg_CLID, CDialog)

CDlg_CLID::CDlg_CLID(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CLID::IDD, pParent)
{

}

CDlg_CLID::~CDlg_CLID()
{
}

void CDlg_CLID::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCurrentLidStatus = 0;
    ulCurrentLidStatus = m_ACPIMailboxManager.stACPIMbx.ulCurrentLidStatus;
    
    m_CLIDCombo.ResetContent();

    m_CLIDCombo.AddString(L"Lid Closed(0)");
    m_CLIDCombo.SetItemData(0,0);

    m_CLIDCombo.AddString(L"Lid Open(1)");
    m_CLIDCombo.SetItemData(1,1);

    if((ulCurrentLidStatus >=0 && ulCurrentLidStatus <= 1))
    {
        m_CLIDCombo.SetCurSel(ulCurrentLidStatus);
    }
    else
    {
        m_CLIDCombo.AddString(L"Invalid Data");
        m_CLIDCombo.SetItemData(2,2);
        m_CLIDCombo.SetCurSel(2);
    }

    UpdateData(FALSE);

}


void CDlg_CLID::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_CLID, m_CLIDCombo);
}


BEGIN_MESSAGE_MAP(CDlg_CLID, CDialog)
END_MESSAGE_MAP()


// CDlg_CLID message handlers
