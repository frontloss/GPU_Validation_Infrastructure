#pragma once


// CTree dialog

class CTree : public CDialog
{
	DECLARE_DYNAMIC(CTree)

public:
	CTree(CWnd* pParent = NULL);   // standard constructor
	virtual ~CTree();

// Dialog Data
	enum { IDD = IDD_ACPI_OP_REGION_DIALOG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnTvnSelchangedTree1(NMHDR *pNMHDR, LRESULT *pResult);
};
