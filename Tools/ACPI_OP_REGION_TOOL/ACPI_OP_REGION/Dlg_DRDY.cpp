// Dlg_DRDY.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_DRDY.h"
#include "stdlib.h"

// CDlg_DRDY dialog

IMPLEMENT_DYNAMIC(CDlg_DRDY, CDialog)

CDlg_DRDY::CDlg_DRDY(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_DRDY::IDD, pParent)
{

}

CDlg_DRDY::~CDlg_DRDY()
{
}

void CDlg_DRDY::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulDRDY = 0;
    ulDRDY = m_ACPIMailboxManager.stACPIMbx.ulDriverReadiness;

    m_DRDYCombo.ResetContent();

    m_DRDYCombo.AddString(L"Driver is not ready (0)");
    m_DRDYCombo.SetItemData(0,0);

    m_DRDYCombo.AddString(L"Driver is ready (1)");
    m_DRDYCombo.SetItemData(1,1);

    if((ulDRDY >=0 && ulDRDY <= 1))
    {
        m_DRDYCombo.SetCurSel(ulDRDY);
    }
    else
    {
        m_DRDYCombo.AddString(L"Invalid Data");
        m_DRDYCombo.SetItemData(2,2);
        m_DRDYCombo.SetCurSel(2);
    }

    UpdateData(FALSE);

}

void CDlg_DRDY::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_DRDY, m_DRDYCombo);
}


BEGIN_MESSAGE_MAP(CDlg_DRDY, CDialog)
END_MESSAGE_MAP()


// CDlg_DRDY message handlers
