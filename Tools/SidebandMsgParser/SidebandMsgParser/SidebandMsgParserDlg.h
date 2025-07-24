
// SidebandMsgParserDlg.h : header file
//

#pragma once
#include "afxwin.h"

#define MAX_MSG_BYTES 256


// CSidebandMsgParserDlg dialog
class CSidebandMsgParserDlg : public CDialogEx
{
// Construction
public:
	CSidebandMsgParserDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_SIDEBANDMSGPARSER_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;
    bool m_bInit;
    void ParseMsg();
    bool ValidateAndExtractData();
    bool ReadMessage(BYTE pbBuff[], PBYTE pout, BYTE byOffset, DWORD dwSize);
    void SetInstructionText();
    void GetClipBoardData();

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnBnClickedButton1();
    // edit box control for display
    CEdit m_editDisplay;
    // edit control for input text
    CEdit m_EditInput;

    DWORD m_dwBuffLen;
    BYTE m_byBuffer[MAX_MSG_BYTES];
    afx_msg void OnBnClickedOk();
    afx_msg void OnBnClickedCancel();
    afx_msg void OnBnClickedBtnLinkAdd();
    afx_msg void OnBnClickedBtnRemoteEdid();
    afx_msg void OnBnClickedBtnEpr();
    afx_msg void OnEnSetfocusEdit1();
    afx_msg void OnBnClickedAllocPayLoad();
    afx_msg void OnBnClickedButton6();
    CButton m_btnTest;
    afx_msg void OnBnClickedCopy();

    afx_msg void OnBnClickedButtonCopy();
    afx_msg void OnBnClickedButtonPaste();
};
