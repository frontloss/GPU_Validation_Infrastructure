#pragma once
#include "afxcmn.h"


// CSeq_Lid dialog

class CSeq_Lid : public CDialog
{
	DECLARE_DYNAMIC(CSeq_Lid)

public:
	CSeq_Lid(CWnd* pParent = NULL);   // standard constructor
	virtual ~CSeq_Lid();
    void Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager);
// Dialog Data
	enum { IDD = IDD_DIALOG_LID_SEQ };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
    CListCtrl m_SeqLidClose;
};
