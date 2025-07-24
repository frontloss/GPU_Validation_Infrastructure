#pragma once
#include "afxwin.h"


// CDlg_DIDL dialog

class CDlg_DIDL : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DIDL)

public:
	CDlg_DIDL(CWnd* pParent = NULL);   // standard constructor
    void CDlg_DIDL::Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_DIDL();

// Dialog Data
	enum { IDD = IDD_DIALOG_DIDL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListBox m_DIDL;
public:
    CEdit m_DIDLEditDesc;
public:
    afx_msg void OnLbnSelchangeStaticDidl();
};
