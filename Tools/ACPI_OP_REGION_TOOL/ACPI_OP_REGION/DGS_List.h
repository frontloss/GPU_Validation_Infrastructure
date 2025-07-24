#pragma once
#include "afxcmn.h"


// CDGS_List dialog

class CDGS_List : public CDialog
{
	DECLARE_DYNAMIC(CDGS_List)

public:
	CDGS_List(CWnd* pParent = NULL);   // standard constructor
	virtual ~CDGS_List();
    void Update(ACPIMbxManager m_ACPIMailboxManager,
                ACPIControlMethodManager m_ACPICMManager);
    void Eval(ACPIMbxManager m_ACPIMailboxManager,
                ACPIControlMethodManager m_ACPICMManager);

// Dialog Data
	enum { IDD = IDD_DIALOG_DGS_NEW };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListCtrl m_DGSListCtrl;
};
