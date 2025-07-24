#pragma once
#include "afxwin.h"


// CDlg_CHPD dialog

class CDlg_CHPD : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CHPD)

public:
	CDlg_CHPD(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CHPD();

// Dialog Data
	enum { IDD = IDD_DIALOG_CHPD };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_CHPDCombo;
};
