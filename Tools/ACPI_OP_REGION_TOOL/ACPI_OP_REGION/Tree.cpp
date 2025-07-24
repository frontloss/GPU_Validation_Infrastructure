// Tree.cpp : implementation file
//

#include "stdafx.h"
#include "ACPI_OP_REGION.h"
#include "Tree.h"


// CTree dialog

IMPLEMENT_DYNAMIC(CTree, CDialog)

CTree::CTree(CWnd* pParent /*=NULL*/)
	: CDialog(CTree::IDD, pParent)
{
    

}

CTree::~CTree()
{
}

void CTree::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CTree, CDialog)
    ON_NOTIFY(TVN_SELCHANGED, IDC_TREE1, &CTree::OnTvnSelchangedTree1)
END_MESSAGE_MAP()


// CTree message handlers

void CTree::OnTvnSelchangedTree1(NMHDR *pNMHDR, LRESULT *pResult)
{
    LPNMTREEVIEW pNMTreeView = reinterpret_cast<LPNMTREEVIEW>(pNMHDR);
        //NM_TREEVIEW* pNMTreeView = (NM_TREEVIEW*)pNMHDR;

         // TODO: Add your control notification handler code here
         //HTREEITEM hItem = m_MFC_Tree.GetSelectedItem();
         //CString strItemText = m_MFC_Tree.GetItemText(hItem);

    //HTREEITEM hItem = GetSelectedItem();
    //CString strItemText = GetItemText(hItem);

         
      //   MessageBox(strItemText);

        *pResult = 0;


    // TODO: Add your control notification handler code here
    *pResult = 0;
}
