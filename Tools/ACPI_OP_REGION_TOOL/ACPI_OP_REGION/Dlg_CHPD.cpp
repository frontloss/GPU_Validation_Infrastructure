// Dlg_CHPD.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CHPD.h"
#include "stdlib.h"


// CDlg_CHPD dialog

IMPLEMENT_DYNAMIC(CDlg_CHPD, CDialog)

CDlg_CHPD::CDlg_CHPD(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CHPD::IDD, pParent)
{

}

CDlg_CHPD::~CDlg_CHPD()
{
}

void CDlg_CHPD::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCurrentHPD = 0;
    ulCurrentHPD = m_ACPIMailboxManager.stACPIMbx.ulCurrentHotPlugIndicator;

    m_CHPDCombo.AddString(L"Hot plug support disabled(0)");
    m_CHPDCombo.SetItemData(0,0);

    m_CHPDCombo.AddString(L"Hot plug support enabled(1)");
    m_CHPDCombo.SetItemData(1,1);

    if((ulCurrentHPD >=0 && ulCurrentHPD <= 1))
    {
        m_CHPDCombo.SetCurSel(ulCurrentHPD);
    }
    else
    {
        m_CHPDCombo.AddString(L"Invalid Data");
        m_CHPDCombo.SetItemData(2,2);
        m_CHPDCombo.SetCurSel(2);
    }

    UpdateData(FALSE);

}


void CDlg_CHPD::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_CHPD, m_CHPDCombo);
}


BEGIN_MESSAGE_MAP(CDlg_CHPD, CDialog)
END_MESSAGE_MAP()


// CDlg_CHPD message handlers
