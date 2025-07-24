#pragma once
#include "afxwin.h"


// CDlg_ARDY dialog

class CDlg_ARDY : public CDialog
{
	DECLARE_DYNAMIC(CDlg_ARDY)

public:
	CDlg_ARDY(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_ARDY();

// Dialog Data
	enum { IDD = IDD_DIALOG_ARDY };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_ARDY;
};
