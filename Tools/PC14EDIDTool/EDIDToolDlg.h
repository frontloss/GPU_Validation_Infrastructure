// EDIDToolDlg.h : header file
// Author: Ganesh Ram S.T

#if !defined(AFX_EDIDTOOLDLG_H__2B85B749_C18A_439C_90BE_35C7F67F5811__INCLUDED_)
#define AFX_EDIDTOOLDLG_H__2B85B749_C18A_439C_90BE_35C7F67F5811__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "Resource.h"
#include "EDIDTool.h"
/////////////////////////////////////////////////////////////////////////////
// CEDIDToolDlg dialog


class CEDIDToolDlg : public CDialog
{
// Construction
public:
	CEDIDToolDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CEDIDToolDlg)
	enum { IDD = IDD_EDIDTOOL_DIALOG };
	CEdit	m_DeviceName;
	CButton	m_Open;
	CButton	m_Save;
	CButton	m_Read;
	CComboBox	m_DeviceId;
	CComboBox	m_DeviceId2;
	CEdit	m_HexValues;
	CEdit	m_TextData;
	CEdit	m_ByteValues;
	CListCtrl	m_ByteDetails;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CEDIDToolDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CEDIDToolDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnOpen();
	afx_msg void OnSave();
	afx_msg void OnRead();
	afx_msg void OnSaveToRegistry();
	afx_msg void OnByteDetails(NMHDR* pNMHDR, LRESULT* pResult);
	afx_msg void OnChangeDeviceId();
	afx_msg void OnCloneEdidButton();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()


		//The Text to be displayed on the Window
	//CString Text;
	
	//The Data for the CEA Extension
	CString CEAText;

	// Vista Escape Call
	void VistaEsc(INT iEsc, INT cbIn, void * pIn, BOOLEAN bDetect);
	
	//Detects the display devices
	void SbDisDetect();

	
	
	//Gets the EDID information from the device
	void GetEdidInfo();
	
	//Open File Dialog
	CString GetFileName(BOOL);
	
	void getByteValues();
	void DisplayInfo();
	void getHexValues();	
	void setDisplayName(ULONG,PORT_TYPES);
	void ClearAll();
	
	INT GetDisplayPortUsed(ULONG ulDisplayID);
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_EDIDTOOLDLG_H__2B85B749_C18A_439C_90BE_35C7F67F5811__INCLUDED_)
