#pragma once
#include "afxwin.h"


// CDlg_CDCK dialog

class CDlg_CDCK : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CDCK)

public:
	CDlg_CDCK(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CDCK();

// Dialog Data
	enum { IDD = IDD_DIALOG_CDCK };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox mCDCKCombo;
};
