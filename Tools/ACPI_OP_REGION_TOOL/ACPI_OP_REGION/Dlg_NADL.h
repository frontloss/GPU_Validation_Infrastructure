#pragma once
#include "afxwin.h"


// CDlg_NADL dialog

class CDlg_NADL : public CDialog
{
	DECLARE_DYNAMIC(CDlg_NADL)

public:
	CDlg_NADL(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_NADL();

// Dialog Data
	enum { IDD = IDD_DIALOG_NADL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListBox m_NADLList;
public:
    CEdit m_NADLEditDesc;
public:
    afx_msg void OnLbnSelchangeListNadl();
};
