// MainTree.cpp : implementation file
//

#include "stdafx.h"
#include "ACPI_OP_REGION.h"
#include "MainTree.h"


// CMainTree dialog

IMPLEMENT_DYNAMIC(CMainTree, CDialog)

CMainTree::CMainTree(CWnd* pParent /*=NULL*/)
	: CDialog(CMainTree::IDD, pParent)
{

}

CMainTree::~CMainTree()
{
}

void CMainTree::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CMainTree, CDialog)
    ON_NOTIFY(TVN_SELCHANGED, IDC_TREE_CTRL, &CMainTree::OnTvnSelchangedTreeCtrl)
END_MESSAGE_MAP()


// CMainTree message handlers

void CMainTree::OnTvnSelchangedTreeCtrl(NMHDR *pNMHDR, LRESULT *pResult)
{
    LPNMTREEVIEW pNMTreeView = reinterpret_cast<LPNMTREEVIEW>(pNMHDR);
    // TODO: Add your control notification handler code here
    *pResult = 0;
}
