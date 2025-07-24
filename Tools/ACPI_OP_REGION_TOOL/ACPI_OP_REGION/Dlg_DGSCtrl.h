#pragma once
#include "afxcmn.h"


// CDlg_DGSCtrl dialog

class CDlg_DGSCtrl : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DGSCtrl)

public:
	CDlg_DGSCtrl(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_DGSCtrl();
    void Eval(ACPIMbxManager m_ACPIMailboxManager,
                ACPIControlMethodManager m_ACPICMManager);
    void Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager);


// Dialog Data
	enum { IDD = IDD_DIALOG_DGS_CTRL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListCtrl m_DGSListCtrl;
};
