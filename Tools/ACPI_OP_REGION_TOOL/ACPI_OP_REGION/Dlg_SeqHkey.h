#pragma once
#include "afxcmn.h"


// CDlg_SeqHkey dialog

class CDlg_SeqHkey : public CDialog
{
	DECLARE_DYNAMIC(CDlg_SeqHkey)

public:
	CDlg_SeqHkey(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_SeqHkey();
    void Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_SEQ_HKEY };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListCtrl m_SeqHkey;
};
