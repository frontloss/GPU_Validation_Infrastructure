// ACPI_OP_REGIONDlg.h : header file
//

#pragma once

#define DLG_MBX_ACPI_MAIN       0x00
#define DLG_MBX_ACPI_DRDY       0x01
#define DLG_MBX_ACPI_CSTS       0x02
#define DLG_MBX_ACPI_CEVT       0x03
#define DLG_MBX_ACPI_DIDL       0x04
#define DLG_MBX_ACPI_CPDL       0x05
#define DLG_MBX_ACPI_CADL       0x06
#define DLG_MBX_ACPI_NADL       0x07
#define DLG_MBX_ACPI_ASLP       0x08
#define DLG_MBX_ACPI_TIDX       0x09
#define DLG_MBX_ACPI_CHPD       0x0A
#define DLG_MBX_ACPI_CLID       0x0B
#define DLG_MBX_ACPI_CDCK       0x0C
#define DLG_MBX_ACPI_NRDY       0x0D
#define DLG_MBX_ACPI_MAX        0xFF

#define DLG_MBX_BIOS_DRV_MAIN       0x100
#define DLG_MBX_BIOS_DRV_ARDY       0x101
#define DLG_MBX_BIOS_DRV_ASLC       0x102
#define DLG_MBX_BIOS_DRV_TCHE       0x103
#define DLG_MBX_BIOS_DRV_ASLI       0x104
#define DLG_MBX_BIOS_DRV_BCLP       0x105
#define DLG_MBX_BIOS_DRV_PFIT       0x106
#define DLG_MBX_BIOS_DRV_CBLV       0x107
#define DLG_MBX_BIOS_DRV_MAX        0x1FF

#define DLG_SCI_EVAL_MAIN           0x200
#define DLG_SCI_EVAL_GET_DVMT       0x201

#define DLG_ACPI_EVAL_MAIN          0x300
#define DLG_ACPI_EVAL_DOD           0x301
#define DLG_ACPI_EVAL_DGS           0x302
#define DLG_ACPI_EVAL_DOS           0x303
#define DLG_ACPI_EVAL_DSS           0x304
#define DLG_ACPI_EVAL_DCS           0x305
#define DLG_ACPI_EVAL_BCL           0x306
#define DLG_ACPI_EVAL_BQC           0x307
#define DLG_ACPI_EVAL_BCM           0x308
#define DLG_ACPI_EVAL_MAX           0x3FF

#define DLG_ACPI_NOTIFICATION       0x400
#define DLG_ACPI_NOT_TRACK_EVNTS    0x401

#define DLG_EVENTS_MAIN             0x500
#define DLG_EVENTS_HOTKEY           0x501
#define DLG_EVENTS_LID_OPEN         0x502
#define DLG_EVENTS_LID_CLOSE        0x503
#define DLG_EVENTS_DOCK             0x504
#define DLG_EVENTS_MAX              0x5FF


#include "..\\..\\..\\LHDM\inc\AcpiCtrlEscape.h"
#include "..\\..\\..\\LHDM\inc\gfxEscape.h"


#include "OPREG_Escape.h"
#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"

#include "LidStatus.h"
#include "Tree.h"
#include "Dlg_ASLP.h"
#include "Dlg_CADL.h"
#include "Dlg_CDCK.h"
#include "Dlg_CEVT.h"
#include "Dlg_CHPD.h"
#include "Dlg_CLID.h"
#include "Dlg_CPDL.h"
#include "Dlg_CSTS.h"
#include "Dlg_DIDL.h"
#include "Dlg_DRDY.h"
#include "Dlg_NADL.h"
#include "Dlg_NDRY.h"
#include "Dlg_TIDX.h"

#include "Dlg_ARDY.h"
#include "Dlg_ALSI.h"
#include "Dlg_ASLC.h"
#include "Dlg_ASLP.h"
#include "Dlg_TCHE.h"
#include "Dlg_CBLV.h"
#include "Dlg_PFIT.h"
#include "Dlg_BCLP.h"

#include "DGS_List.h"
#include "Dlg_DOS.h"
#include "Dlg_BCLCtrl.h"
#include "Dlg_BCM_Ctrl.h"
#include "Dlg_DOD_Ctrl.h"
#include "Dlg_DSS_Ctrl.h"

#include "Seq_Lid.h"
#include "Dlg_SeqHkey.h"

#include "afxcmn.h"

// CACPI_OP_REGIONDlg dialog
class CACPI_OP_REGIONDlg : public CDialog
{
// Construction
public:
	CACPI_OP_REGIONDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_ACPI_OP_REGION_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
    afx_msg void OnBnClickedOk();
    CLidStatus CLid;

    //Mailbox 1 handles
    CDlg_ASLP cDlgASLP;
    CDlg_CADL cDlgCADL;
    CDlg_CDCK cDlgCDCK;
    CDlg_CEVT cDlgCEVT;
    CDlg_CHPD cDlgCHPD;
    CDlg_CLID cDlgCLID;
    CDlg_CPDL cDlgCPDL;
    CDlg_CSTS cDlgCSTS;
    CDlg_DIDL cDlgDIDL;
    CDlg_DRDY cDlgDRDY;
    CDlg_NADL cDlgNADL;
    CDlg_NDRY cDlgNRDY;
    CDlg_TIDX cDlgTIDX;

    //Mailbox 3 handles
    CDlg_ARDY cDlgARDY;
    CDlg_ASLC cDlgASLC;
    CDlg_TCHE cDlgTCHE;
    CDlg_ALSI cDlgASLI;
    Dlg_BCLP cDlgBCLP;
    CDlg_PFIT cDlgPFIT;
    CDlg_CBLV cDlgCBLV;

    //ACPI Control Methods
    CDGS_List cDlgDGSCtrl;
    CDlg_DOS  cDlgDOS;
    CDlg_BCLCtrl cDlg_BCLCtrl;
    CDlg_BCM_Ctrl cDlg_BCMCtrl;
    CDlg_DSS_Ctrl cDlg_DSSCtrl;
    CDlg_DOD_Ctrl cDlg_DODCtrl;    

    CSeq_Lid cDlgLidClose; //Lid Close (switch)
    CDlg_SeqHkey cDlgHkey;

    ACPIMbxManager m_ACPIMbxMngr;
    ACPIControlMethodManager m_ACPICMMngr;

    ULONG bFromFile;
    //CTree m_Tree;

public:
    //CTreeCtrl m_TreeCtrl;
public:
    CTreeCtrl m_MainTreeCtrl;
public:
    afx_msg void OnTvnSelchangedTreeCtrl(NMHDR *pNMHDR, LRESULT *pResult);
public:
    afx_msg void OnBnClickedButtonRefresh();
    void UpdatePage(DWORD dwPage);
    DWORD dwLastSel;
public:
    afx_msg void OnBnClickedButtonLoad();

    OPENFILENAME ofn;
public:
    afx_msg void OnLoadFromfile();
public:
    afx_msg void OnLoadFromsystem();
public:
    afx_msg void OnFileSave32773();
};
