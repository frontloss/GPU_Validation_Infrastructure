#pragma once


// CDlg_DOD dialog

class CDlg_DOD : public CDialog
{
	DECLARE_DYNAMIC(CDlg_DOD)

public:
	CDlg_DOD(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDlg_DOD();

// Dialog Data
	enum { IDD = IDD_DIALOG_DIDL };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
};
