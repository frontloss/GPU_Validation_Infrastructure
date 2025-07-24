#pragma once
#include "afxwin.h"


// CDlg_DOD_Ctrl dialog

class CDlg_DOD_Ctrl : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DOD_Ctrl)

public:
	CDlg_DOD_Ctrl(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_DOD_Ctrl();
    void Update(ACPIControlMethodManager m_ACPICMManager);
    void Eval(ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_DOD_CTRL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListBox m_DODList;
public:
    CEdit m_DODComment;
public:
    afx_msg void OnLbnSelchangeListDod();
};
