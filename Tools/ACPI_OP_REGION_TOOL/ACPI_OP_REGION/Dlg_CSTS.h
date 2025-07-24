#pragma once
#include "afxwin.h"


// CDlg_CSTS dialog

class CDlg_CSTS : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CSTS)

public:
	CDlg_CSTS(CWnd* pParent = NULL);   // standard constructor
    void CDlg_CSTS::Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CSTS();

// Dialog Data
	enum { IDD = IDD_DIALOG_CSTS };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_CSTSCombo;
};
