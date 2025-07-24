#pragma once
#include "afxwin.h"


// CDlg_ASLC dialog

class CDlg_ASLC : public CDialog
{
	DECLARE_DYNAMIC(CDlg_ASLC)

public:
	CDlg_ASLC(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_ASLC();

// Dialog Data
	enum { IDD = IDD_DIALOG_ASLC };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_ASLCComboALS;
public:
    CComboBox m_ASLCComboBKT;
public:
    CComboBox m_ASLCComboPFIT;
public:
    afx_msg void OnStnClickedStaticDrdy1();
};
