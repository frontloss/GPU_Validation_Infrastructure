#pragma once


// Dlg_BCLP dialog

class Dlg_BCLP : public CDialog
{
	DECLARE_DYNAMIC(Dlg_BCLP)

public:
	Dlg_BCLP(CWnd* pParent = NULL);   // standard constructor
    void Update(ACPIMbxManager m_ACPIMailboxManager);
	virtual ~Dlg_BCLP();

// Dialog Data
	enum { IDD = IDD_DIALOG_BCLP };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CString m_BCLPValue;
};
