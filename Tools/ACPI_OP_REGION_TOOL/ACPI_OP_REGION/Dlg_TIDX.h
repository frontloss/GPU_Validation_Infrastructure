#pragma once
#include "afxwin.h"


// CDlg_TIDX dialog

class CDlg_TIDX : public CDialog
{
	DECLARE_DYNAMIC(CDlg_TIDX)

public:
	CDlg_TIDX(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_TIDX();

// Dialog Data
	enum { IDD = IDD_DIALOG_TIDX };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_TIDXCombo;
};
