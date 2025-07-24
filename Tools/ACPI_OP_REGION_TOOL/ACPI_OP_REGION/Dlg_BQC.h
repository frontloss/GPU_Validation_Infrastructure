#pragma once


// CDlg_BQC dialog

class CDlg_BQC : public CDialog
{
	DECLARE_DYNAMIC(CDlg_BQC)

public:
	CDlg_BQC(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_BQC();

// Dialog Data
	enum { IDD = IDD_DIALOG_CLID };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
};
