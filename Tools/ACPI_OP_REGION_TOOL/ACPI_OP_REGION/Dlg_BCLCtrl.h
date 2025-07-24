#pragma once
#include "afxcmn.h"


// CDlg_BCLCtrl dialog

class CDlg_BCLCtrl : public CDialog
{
	DECLARE_DYNAMIC(CDlg_BCLCtrl)

public:
	CDlg_BCLCtrl(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_BCLCtrl();
    void Update(ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_BCL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListCtrl m_BCLListCtrl;
};
