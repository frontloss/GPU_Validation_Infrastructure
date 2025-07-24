#pragma once
#include "afxwin.h"


// CDlg_PFIT dialog

class CDlg_PFIT : public CDialog
{
	DECLARE_DYNAMIC(CDlg_PFIT)

public:
	CDlg_PFIT(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_PFIT();

// Dialog Data
	enum { IDD = IDD_DIALOG_PFIT };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_PFITComboCenter;
public:
    CComboBox m_PFITComboTxtModeStr;
public:
    CComboBox m_PFITComboGfxModeStr;
};
