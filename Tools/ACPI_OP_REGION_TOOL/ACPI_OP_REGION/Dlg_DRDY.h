#pragma once
#include "afxwin.h"


// CDlg_DRDY dialog

class CDlg_DRDY : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DRDY)

public:
	CDlg_DRDY(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_DRDY();

// Dialog Data
	enum { IDD = IDD_DIALOG_DRDY };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_DRDYCombo;
};
