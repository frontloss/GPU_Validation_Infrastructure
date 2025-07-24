// LidStatus.cpp : implementation file
//

#include "stdafx.h"
#include "ACPI_OP_REGION.h"
#include "LidStatus.h"


// CLidStatus dialog

IMPLEMENT_DYNAMIC(CLidStatus, CDialog)

CLidStatus::CLidStatus(CWnd* pParent /*=NULL*/)
	: CDialog(CLidStatus::IDD, pParent)
{

}

CLidStatus::~CLidStatus()
{
}

void CLidStatus::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CLidStatus, CDialog)
    ON_EN_CHANGE(IDC_EDIT1, &CLidStatus::OnEnChangeEdit1)
    ON_STN_CLICKED(IDC_CLID_LABEL, &CLidStatus::OnStnClickedClidLabel)
    ON_NOTIFY(TVN_SELCHANGED, IDC_TREE1, &CLidStatus::OnTvnSelchangedTree1)
END_MESSAGE_MAP()


// CLidStatus message handlers

void CLidStatus::OnEnChangeEdit1()
{
    // TODO:  If this is a RICHEDIT control, the control will not
    // send this notification unless you override the CDialog::OnInitDialog()
    // function and call CRichEditCtrl().SetEventMask()
    // with the ENM_CHANGE flag ORed into the mask.

    // TODO:  Add your control notification handler code here
}

void CLidStatus::OnStnClickedClidLabel()
{
    // TODO: Add your control notification handler code here
}

void CLidStatus::OnTvnSelchangedTree1(NMHDR *pNMHDR, LRESULT *pResult)
{
    LPNMTREEVIEW pNMTreeView = reinterpret_cast<LPNMTREEVIEW>(pNMHDR);
    // TODO: Add your control notification handler code here
    *pResult = 0;
}
