#pragma once


// CMainTree dialog

class CMainTree : public CDialog
{
	DECLARE_DYNAMIC(CMainTree)

public:
	CMainTree(CWnd* pParent = NULL);   // standard constructor
	virtual ~CMainTree();

// Dialog Data
	enum { IDD = IDD_ACPI_OP_REGION_DIALOG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnTvnSelchangedTreeCtrl(NMHDR *pNMHDR, LRESULT *pResult);
};
