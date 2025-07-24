#pragma once


// CLidStatus dialog

class CLidStatus : public CDialog
{
	DECLARE_DYNAMIC(CLidStatus)

public:
	CLidStatus(CWnd* pParent = NULL);   // standard constructor
	virtual ~CLidStatus();

// Dialog Data
	enum { IDD = IDD_DIALOG_LID };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnEnChangeEdit1();
public:
    afx_msg void OnStnClickedClidLabel();
public:
    afx_msg void OnTvnSelchangedTree1(NMHDR *pNMHDR, LRESULT *pResult);
};
