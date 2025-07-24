#pragma once
#include "afxwin.h"


// CDlg_DSS_Ctrl dialog

class CDlg_DSS_Ctrl : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DSS_Ctrl)

public:
	CDlg_DSS_Ctrl(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_DSS_Ctrl();
    void Update(ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_DSS_CTRL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_DSSACPIID;
public:
    CComboBox m_DSSVal;
};
