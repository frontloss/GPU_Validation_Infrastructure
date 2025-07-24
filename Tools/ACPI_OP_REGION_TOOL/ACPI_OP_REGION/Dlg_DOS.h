#pragma once
#include "afxwin.h"


// CDlg_DOS dialog

class CDlg_DOS : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DOS)

public:
	CDlg_DOS(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_DOS();
    void Update(ACPIControlMethodManager m_ACPICMMngrMailboxManager);
    void Eval(ACPIControlMethodManager m_ACPICMMngrMailboxManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_DOS };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_Combo_DOS_DispSW;
public:
    CComboBox m_Combo_DOS_AutoDim;
public:
    afx_msg void OnBnClickedButton1();
public:
    CComboBox m_DOS_Switch;
};
