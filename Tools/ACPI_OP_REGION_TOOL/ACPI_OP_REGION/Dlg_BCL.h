#pragma once


// CDlg_BCL dialog

class CDlg_BCL : public CDialog
{
	DECLARE_DYNAMIC(CDlg_BCL)

public:
	CDlg_BCL(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_BCL();
    void Update(ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_DGS };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    
};
