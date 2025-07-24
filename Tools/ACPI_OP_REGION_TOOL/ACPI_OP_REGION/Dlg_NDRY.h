#pragma once
#include "afxwin.h"


// CDlg_NDRY dialog

class CDlg_NDRY : public CDialog
{
	DECLARE_DYNAMIC(CDlg_NDRY)

public:
	CDlg_NDRY(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_NDRY();

// Dialog Data
	enum { IDD = IDD_DIALOG_NRDY };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_NRDYCombo;
};
