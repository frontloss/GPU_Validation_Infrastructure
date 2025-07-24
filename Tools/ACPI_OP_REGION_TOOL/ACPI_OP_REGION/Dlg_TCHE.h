#pragma once
#include "afxwin.h"


// CDlg_TCHE dialog

class CDlg_TCHE : public CDialog
{
	DECLARE_DYNAMIC(CDlg_TCHE)

public:
	CDlg_TCHE(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_TCHE();

// Dialog Data
	enum { IDD = IDD_DIALOG_TCHE };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CComboBox m_ASLCComboALS;
public:
    CComboBox m_ASLCComboBKT;
public:
    CComboBox m_ASLCComboPFIT;
};
