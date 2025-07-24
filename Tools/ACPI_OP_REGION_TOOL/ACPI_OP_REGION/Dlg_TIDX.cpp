// Dlg_TIDX.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_TIDX.h"
#include "stdlib.h"


// CDlg_TIDX dialog

IMPLEMENT_DYNAMIC(CDlg_TIDX, CDialog)

CDlg_TIDX::CDlg_TIDX(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_TIDX::IDD, pParent)
{

}

CDlg_TIDX::~CDlg_TIDX()
{
}

void CDlg_TIDX::Update(ACPIMbxManager m_ACPIMailboxManager)
{

    ULONG ulTIDX = 0;
    ulTIDX = m_ACPIMailboxManager.stACPIMbx.ulToggleTableIndex;

    m_TIDXCombo.ResetContent();

    m_TIDXCombo.AddString(L"Toggle Table 0");
    m_TIDXCombo.SetItemData(0,0);

    m_TIDXCombo.AddString(L"Toggle Table 1");
    m_TIDXCombo.SetItemData(1,1);

    m_TIDXCombo.AddString(L"Toggle Table 2");
    m_TIDXCombo.SetItemData(2,2);

    m_TIDXCombo.AddString(L"Toggle Table 3");
    m_TIDXCombo.SetItemData(3,3);

    if((ulTIDX >=0 && ulTIDX <= 3))
    {
        m_TIDXCombo.SetCurSel(ulTIDX);
    }
    else
    {
        m_TIDXCombo.AddString(L"Invalid Data");
        m_TIDXCombo.SetItemData(4,4);
        m_TIDXCombo.SetCurSel(4);
    }

    UpdateData(FALSE);

}

void CDlg_TIDX::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_TIDX, m_TIDXCombo);
}


BEGIN_MESSAGE_MAP(CDlg_TIDX, CDialog)
END_MESSAGE_MAP()


// CDlg_TIDX message handlers
