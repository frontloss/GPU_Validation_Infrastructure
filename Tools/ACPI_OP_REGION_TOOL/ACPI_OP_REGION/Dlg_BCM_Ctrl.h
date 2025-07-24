#pragma once
#include "afxwin.h"


// CDlg_BCM_Ctrl dialog

class CDlg_BCM_Ctrl : public CDialog
{
	DECLARE_DYNAMIC(CDlg_BCM_Ctrl)

public:
	CDlg_BCM_Ctrl(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_BCM_Ctrl();
    void Update(ACPIControlMethodManager m_ACPICMManager);
    void Eval(ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_BCM_CTRL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_BCM_Ctrl;
};
