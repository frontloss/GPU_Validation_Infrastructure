#pragma once
#include "afxwin.h"


// CDlg_CADL dialog

class CDlg_CADL : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CADL)

public:
	CDlg_CADL(CWnd* pParent = NULL);   // standard constructor
    void CDlg_CADL::Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CADL();

// Dialog Data
	enum { IDD = IDD_DIALOG_CADL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListBox m_CADLList;
public:
    afx_msg void OnStnClickedStaticAslp();
public:
    afx_msg void OnLbnSelchangeListAslp();
public:
    CEdit mCADLDesc;
};
