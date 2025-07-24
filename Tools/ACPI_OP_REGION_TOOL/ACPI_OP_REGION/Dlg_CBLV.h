#pragma once


// CDlg_CBLV dialog

class CDlg_CBLV : public CDialog
{
	DECLARE_DYNAMIC(CDlg_CBLV)

public:
	CDlg_CBLV(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_CBLV();

// Dialog Data
	enum { IDD = IDD_DIALOG_CBLV };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CString m_CBLVValue;
};
