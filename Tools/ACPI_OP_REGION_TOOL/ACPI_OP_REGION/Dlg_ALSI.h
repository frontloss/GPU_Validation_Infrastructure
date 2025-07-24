#pragma once


// CDlg_ALSI dialog

class CDlg_ALSI : public CDialog
{
	DECLARE_DYNAMIC(CDlg_ALSI)

public:
	CDlg_ALSI(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~CDlg_ALSI();

// Dialog Data
	enum { IDD = IDD_DIALOG_ASLI };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    ULONG m_ALSValue;
};
