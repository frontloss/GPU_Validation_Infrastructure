#pragma once


// CDlg_ASLP dialog

class CDlg_ASLP : public CDialog
{
	DECLARE_DYNAMIC(CDlg_ASLP)

public:
	CDlg_ASLP(CWnd* pParent = NULL);   // standard constructor
    void CDlg_ASLP::Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_ASLP();

// Dialog Data
	enum { IDD = IDD_DIALOG_ASLP };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()

public:
    ULONG m_ASLPValue;
};
