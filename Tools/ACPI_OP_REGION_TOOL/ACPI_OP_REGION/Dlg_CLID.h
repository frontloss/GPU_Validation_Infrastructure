#pragma once
#include "afxwin.h"


// CDlg_CLID dialog

class CDlg_CLID : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CLID)

public:
	CDlg_CLID(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CLID();

// Dialog Data
	enum { IDD = IDD_DIALOG_CLID };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_CLIDCombo;
};
