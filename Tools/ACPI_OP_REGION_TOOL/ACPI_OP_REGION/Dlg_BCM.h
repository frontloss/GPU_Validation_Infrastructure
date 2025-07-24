#pragma once


// CDlg_BCM dialog

class CDlg_BCM : public CDialog
{
	DECLARE_DYNAMIC(CDlg_BCM)

public:
	CDlg_BCM(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_BCM();

// Dialog Data
	enum { IDD = IDD_DIALOG_CLID };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
};
