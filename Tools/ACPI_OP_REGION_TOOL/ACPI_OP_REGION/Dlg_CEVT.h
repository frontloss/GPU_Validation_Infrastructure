#pragma once
#include "afxwin.h"


// CDlg_CEVT dialog

class CDlg_CEVT : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CEVT)

public:
	CDlg_CEVT(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CEVT();

// Dialog Data
	enum { IDD = IDD_DIALOG_CEVT };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_CEVTCombo;
};
