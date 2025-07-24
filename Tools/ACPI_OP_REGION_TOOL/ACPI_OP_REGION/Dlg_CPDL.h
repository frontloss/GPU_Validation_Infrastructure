#pragma once
#include "afxwin.h"


// CDlg_CPDL dialog

class CDlg_CPDL : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CPDL)

public:
	CDlg_CPDL(CWnd* pParent = NULL);   // standard constructor
    void CDlg_CPDL::Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CPDL();

// Dialog Data
	enum { IDD = IDD_DIALOG_CPDL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListBox m_CPDLList;
public:
    CEdit m_CPDLEditDesc;
public:
    afx_msg void OnLbnSelchangeListCpdl();
};
