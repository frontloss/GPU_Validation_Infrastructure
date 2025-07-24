// ACPI_OP_REGIONDlg.cpp : implementation file
//

#include "stdafx.h"

#include "ACPI_OP_REGION.h"
#include "ACPI_OP_REGIONDlg.h"

#ifndef NTSTATUS
#define NTSTATUS int
#endif
#include "inc\d3dkmthk.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

HMODULE hGdi32 = NULL;
PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter = NULL;
PFND3DKMT_ESCAPE D3DKmtEscape = NULL;
PFND3DKMT_CLOSEADAPTER CloseAdapter = NULL;
PFND3DKMT_INVALIDATEACTIVEVIDPN InvalidateActiveVidPnThunk = NULL;

#define MAX_ASSUMED_DEVICES 8

// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// CACPI_OP_REGIONDlg dialog




CACPI_OP_REGIONDlg::CACPI_OP_REGIONDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CACPI_OP_REGIONDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CACPI_OP_REGIONDlg::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    //DDX_Control(pDX, IDC_TREE1, m_TreeCtrl);
    DDX_Control(pDX, IDC_TREE_CTRL, m_MainTreeCtrl);
}

BEGIN_MESSAGE_MAP(CACPI_OP_REGIONDlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
    ON_BN_CLICKED(IDOK, &CACPI_OP_REGIONDlg::OnBnClickedOk)
    ON_NOTIFY(TVN_SELCHANGED, IDC_TREE_CTRL, &CACPI_OP_REGIONDlg::OnTvnSelchangedTreeCtrl)
    ON_BN_CLICKED(IDC_BUTTON_REFRESH, &CACPI_OP_REGIONDlg::OnBnClickedButtonRefresh)
    ON_BN_CLICKED(IDC_BUTTON_LOAD, &CACPI_OP_REGIONDlg::OnBnClickedButtonLoad)
    ON_COMMAND(ID_LOAD_FROMFILE, &CACPI_OP_REGIONDlg::OnLoadFromfile)
    ON_COMMAND(ID_LOAD_FROMSYSTEM, &CACPI_OP_REGIONDlg::OnLoadFromsystem)
    ON_COMMAND(ID_FILE_SAVE32773, &CACPI_OP_REGIONDlg::OnFileSave32773)
END_MESSAGE_MAP()


// CACPI_OP_REGIONDlg message handlers

BOOL CACPI_OP_REGIONDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

    //get the OS version
    //6 - vista
    //5 -xp

    hGdi32 = LoadLibraryA("gdi32.dll");
    OpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32,"D3DKMTOpenAdapterFromHdc");
    D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32,"D3DKMTEscape");
    CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32,"D3DKMTCloseAdapter");
      
    //Add Items to CTree
    TVINSERTSTRUCT tvACPIMbx;
    tvACPIMbx.hParent = NULL;
    tvACPIMbx.hInsertAfter = NULL;
    tvACPIMbx.item.mask = TVIF_TEXT;
    tvACPIMbx.item.pszText = _T("Public ACPI Methods Mailbox");
    
    
    //Init params
    bFromFile = TRUE;

    //Initialize Tree Control
    HTREEITEM hItemACPIMbx = m_MainTreeCtrl.InsertItem(&tvACPIMbx);
    m_MainTreeCtrl.SetItemData(hItemACPIMbx, 0);

    TVINSERTSTRUCT hChildItem;
    hChildItem.hParent = hItemACPIMbx;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;
    hChildItem.item.pszText = _T("Driver Readiness (DRDY)");
    
    HTREEITEM hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_DRDY);

    hChildItem.item.pszText = _T("Notification Status (CSTS)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CSTS);

    hChildItem.item.pszText = _T("Current Event (CEVT)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CEVT);

    hChildItem.item.pszText = _T("Supported Displays Devices (DIDL)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_DIDL);

    hChildItem.item.pszText = _T("Currently Attached Display List (CPDL)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CPDL);

    hChildItem.item.pszText = _T("Currently Active Display List (CADL)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CADL);

    hChildItem.item.pszText = _T("Next Active Display List (NADL)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_NADL);

    hChildItem.item.pszText = _T("ASL Sleep Time Out (ASLP)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_ASLP);

    hChildItem.item.pszText = _T("Toggle Table Index (TIDX)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_TIDX);

    hChildItem.item.pszText = _T("Current Hotplug Enable Indicator (CHPD)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CHPD);

    hChildItem.item.pszText = _T("Current Lid State Indicator (CLID)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CLID);

    hChildItem.item.pszText = _T("Current Docking State Indicator (CDCK)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_CDCK);

    hChildItem.item.pszText = _T("Driver Status (NRDY)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_ACPI_NRDY);


    //
    // Add Mailbox to Tree
    //

    TVINSERTSTRUCT tvBIOSDrvMbx;
    tvBIOSDrvMbx.hParent = NULL;
    tvBIOSDrvMbx.hInsertAfter = NULL;
    tvBIOSDrvMbx.item.mask = TVIF_TEXT;
    tvBIOSDrvMbx.item.pszText = _T("BIOS / Driver Communication Mailbox");
    
    
    //Initialize Tree Control
    HTREEITEM hItemBIOSDrvMbx = m_MainTreeCtrl.InsertItem(&tvBIOSDrvMbx);
    m_MainTreeCtrl.SetItemData(hItemBIOSDrvMbx, 100);

    hChildItem.hParent = hItemBIOSDrvMbx;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;
    hChildItem.item.pszText = _T("Driver Readiness (ARDY)");
    
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_ARDY);

    hChildItem.item.pszText = _T("ASLE Interrupt Command Status (ASLC)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_ASLC);

    hChildItem.item.pszText = _T("Technology Enabled Indicator (TCHE)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_TCHE);

    hChildItem.item.pszText = _T("Current ASLE Luminance Reading (ASLI)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_ASLI);

    hChildItem.item.pszText = _T("Backlight Brightness to set (BCLP)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_BCLP);

    hChildItem.item.pszText = _T("Panel Fitting current state or request (PFIT)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_PFIT);

    hChildItem.item.pszText = _T("Current Brightness Level (CBLV)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_CBLV);


    //
    // Tree Item #3: Add SCI Evaluation 
    //

/*    TVINSERTSTRUCT tvSCIEval;
    tvSCIEval.hParent = NULL;
    tvSCIEval.hInsertAfter = NULL;
    tvSCIEval.item.mask = TVIF_TEXT;
    tvSCIEval.item.pszText = _T("SCI Evaluation");

    //Initialize Tree Control
    HTREEITEM hItemSCIEval = m_MainTreeCtrl.InsertItem(&tvSCIEval);
    m_MainTreeCtrl.SetItemData(hItemBIOSDrvMbx, DLG_SCI_EVAL_MAIN);

    hChildItem.hParent = hItemSCIEval;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;
    hChildItem.item.pszText = _T("Get DVMT Settings");
    
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_SCI_EVAL_GET_DVMT); (/

    /*hChildItem.item.pszText = _T("ASLE Interrupt Command Status (ASLC)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_ASLC);

    hChildItem.item.pszText = _T("Technology Enabled Indicator (TCHE)");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_MBX_BIOS_DRV_TCHE);*/

    //
    // Tree Item #4: ACPI Control Methods
    //

    TVINSERTSTRUCT tvACPICMEval;
    tvACPICMEval.hParent = NULL;
    tvACPICMEval.hInsertAfter = NULL;
    tvACPICMEval.item.mask = TVIF_TEXT;
    tvACPICMEval.item.pszText = _T("ACPI Control Methods Evaluation");

    //Initialize Tree Control
    HTREEITEM hItemACPICMEval = m_MainTreeCtrl.InsertItem(&tvACPICMEval);
    m_MainTreeCtrl.SetItemData(hItemACPICMEval, DLG_ACPI_EVAL_MAIN);

    hChildItem.hParent = hItemACPICMEval;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;

    hChildItem.item.pszText = _T("_DOD");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_DOD);

    hChildItem.item.pszText = _T("_DGS");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_DGS);

    hChildItem.item.pszText = _T("_DOS");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_DOS);

    hChildItem.item.pszText = _T("_DSS");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_DSS);

    hChildItem.item.pszText = _T("_BCL");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_BCL);

    /*hChildItem.item.pszText = _T("_BQC");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_BQC); */

    hChildItem.item.pszText = _T("_BCM");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_EVAL_BCM);


    //
    // Tree Item #5: Add Notifications
    //


    /*TVINSERTSTRUCT tvACPINotification;
    tvACPINotification.hParent = NULL;
    tvACPINotification.hInsertAfter = NULL;
    tvACPINotification.item.mask = TVIF_TEXT;
    tvACPINotification.item.pszText = _T("ACPI Notifications");

    HTREEITEM hItemACPINot = m_MainTreeCtrl.InsertItem(&tvACPINotification);
    m_MainTreeCtrl.SetItemData(hItemACPINot, DLG_ACPI_NOTIFICATION);

    hChildItem.hParent = hItemACPINot;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;

    hChildItem.item.pszText = _T("Track ACPI Notifications");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_ACPI_NOT_TRACK_EVNTS); */

    //
    // Tree Item #6: Add Events
    //

    TVINSERTSTRUCT tvEvents;
    tvEvents.hParent = NULL;
    tvEvents.hInsertAfter = NULL;
    tvEvents.item.mask = TVIF_TEXT;
    tvEvents.item.pszText = _T("Events (Auto-Debug)");

    HTREEITEM hItemEvents = m_MainTreeCtrl.InsertItem(&tvEvents);
    m_MainTreeCtrl.SetItemData(hItemEvents, DLG_EVENTS_MAIN);

    hChildItem.hParent = hItemEvents;
    hChildItem.hInsertAfter = NULL;
    hChildItem.item.mask = TVIF_TEXT;
    hChildItem.item.pszText = _T("ACPI Hotkey");

    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_EVENTS_HOTKEY);

    hChildItem.item.pszText = _T("Lid Switch");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_EVENTS_LID_CLOSE);

    /*hChildItem.item.pszText = _T("Lid Open");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_EVENTS_LID_OPEN);*/

    hChildItem.item.pszText = _T("Dock");
    hTreeItem = m_MainTreeCtrl.InsertItem(&hChildItem);
    m_MainTreeCtrl.SetItemData(hTreeItem, DLG_EVENTS_DOCK);


    //Expand the tree control
    //m_MainTreeCtrl.Expand(hItemACPIMbx, TVE_EXPAND);
    //m_MainTreeCtrl.Expand(hItemBIOSDrvMbx, TVE_EXPAND);

    //Initialize Child Windows
    CWnd *cwPlaceHolder = GetDlgItem(IDC_MAINFRAME);
    RECT rcPlaceHolderRect;
    ::GetWindowRect(cwPlaceHolder->m_hWnd, &rcPlaceHolderRect);
    //::MapWindowPoints(NULL,this->m_hWnd,(LPPOINT)&rcPlaceHolderRect,2);

    CLid.Create(IDD_DIALOG_LID, this);
    ::MoveWindow(CLid.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    CLid.ShowWindow(SW_HIDE);

    cDlgASLP.Create(IDD_DIALOG_ASLP,this);
    ::MoveWindow(cDlgASLP.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgASLP.ShowWindow(SW_HIDE);

    cDlgCADL.Create(IDD_DIALOG_CADL,this);
    ::MoveWindow(cDlgCADL.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCADL.ShowWindow(SW_HIDE);

    cDlgCDCK.Create(IDD_DIALOG_CDCK,this);
    ::MoveWindow(cDlgCDCK.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCDCK.ShowWindow(SW_HIDE);

    cDlgCEVT.Create(IDD_DIALOG_CEVT,this);
    ::MoveWindow(cDlgCEVT.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCEVT.ShowWindow(SW_HIDE);

    cDlgCHPD.Create(IDD_DIALOG_CHPD,this);
    ::MoveWindow(cDlgCHPD.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCHPD.ShowWindow(SW_HIDE);

    cDlgCLID.Create(IDD_DIALOG_CLID,this);
    ::MoveWindow(cDlgCLID.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCLID.ShowWindow(SW_HIDE);

    cDlgCPDL.Create(IDD_DIALOG_CPDL,this);
    ::MoveWindow(cDlgCPDL.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCPDL.ShowWindow(SW_HIDE);

    cDlgCSTS.Create(IDD_DIALOG_CSTS,this);
    ::MoveWindow(cDlgCSTS.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgCSTS.ShowWindow(SW_HIDE);

    cDlgDIDL.Create(IDD_DIALOG_DIDL,this);
    ::MoveWindow(cDlgDIDL.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgDIDL.ShowWindow(SW_HIDE);

    cDlgDRDY.Create(IDD_DIALOG_DRDY,this);
    ::MoveWindow(cDlgDRDY.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgDRDY.ShowWindow(SW_HIDE);

    cDlgNADL.Create(IDD_DIALOG_NADL,this);
    ::MoveWindow(cDlgNADL.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgNADL.ShowWindow(SW_HIDE);

    cDlgNRDY.Create(IDD_DIALOG_NRDY,this);
    ::MoveWindow(cDlgNRDY.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgNRDY.ShowWindow(SW_HIDE);

    cDlgTIDX.Create(IDD_DIALOG_TIDX,this);
    ::MoveWindow(cDlgTIDX.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    //Mbx #3
    cDlgARDY.Create(IDD_DIALOG_ARDY,this);
    ::MoveWindow(cDlgARDY.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgASLC.Create(IDD_DIALOG_ASLC,this);
    ::MoveWindow(cDlgASLC.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgASLI.Create(IDD_DIALOG_ASLI,this);
    ::MoveWindow(cDlgASLI.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgBCLP.Create(IDD_DIALOG_BCLP,this);
    ::MoveWindow(cDlgBCLP.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgCBLV.Create(IDD_DIALOG_CBLV,this);
    ::MoveWindow(cDlgCBLV.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgPFIT.Create(IDD_DIALOG_PFIT,this);
    ::MoveWindow(cDlgPFIT.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);

    cDlgTCHE.Create(IDD_DIALOG_TCHE,this);
    ::MoveWindow(cDlgTCHE.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
    (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);


    //Create Windows: ACPI control Methods
    cDlgDGSCtrl.Create(IDD_DIALOG_DGS_CTRL,this);
    ::MoveWindow(cDlgDGSCtrl.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgDGSCtrl.ShowWindow(SW_HIDE);

    cDlgDOS.Create(IDD_DIALOG_DOS,this);
    ::MoveWindow(cDlgDOS.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgDOS.ShowWindow(SW_HIDE);

    cDlg_BCLCtrl.Create(IDD_DIALOG_BCL,this);
    ::MoveWindow(cDlg_BCLCtrl.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlg_BCLCtrl.ShowWindow(SW_HIDE);

    cDlg_BCMCtrl.Create(IDD_DIALOG_BCM_CTRL,this);
    ::MoveWindow(cDlg_BCMCtrl.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlg_BCMCtrl.ShowWindow(SW_HIDE);

    cDlg_DODCtrl.Create(IDD_DIALOG_DOD_CTRL,this);
    ::MoveWindow(cDlg_DODCtrl.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlg_DODCtrl.ShowWindow(SW_HIDE);

    cDlg_DSSCtrl.Create(IDD_DIALOG_DSS_CTRL,this);
    ::MoveWindow(cDlg_DSSCtrl.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlg_DSSCtrl.ShowWindow(SW_HIDE);

    //Add Event Sequence Windows
    cDlgLidClose.Create(IDD_DIALOG_LID_SEQ,this);
    ::MoveWindow(cDlgLidClose.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgLidClose.ShowWindow(SW_HIDE);
    
    cDlgHkey.Create(IDD_DIALOG_SEQ_HKEY,this);
    ::MoveWindow(cDlgHkey.m_hWnd,rcPlaceHolderRect.left + 4,rcPlaceHolderRect.top + 4, 
        (rcPlaceHolderRect.right-rcPlaceHolderRect.left), (rcPlaceHolderRect.bottom-rcPlaceHolderRect.top),TRUE);
    cDlgHkey.ShowWindow(SW_HIDE);


    //Other windows
    cDlgTIDX.ShowWindow(SW_HIDE); //to remove??

    //Load Default Data (Call Escape)
    if(NULL != OpenAdapter)
    {
        bool bACPIMbxValid = m_ACPIMbxMngr.GetMailboxData();  
        bFromFile = FALSE;
    }

    return TRUE;  // return TRUE  unless you set the focus to a control
}

void CACPI_OP_REGIONDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CACPI_OP_REGIONDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CACPI_OP_REGIONDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void CACPI_OP_REGIONDlg::OnBnClickedOk()
{
    // TODO: Add your control notification handler code here
    //if version is Xp
    //CDC *pdc = GetDC();
    //HDC hDc= pdc->m_hDC;

    //Initialize Mailbox
    bool bACPIMbxValid = m_ACPIMbxMngr.GetMailboxData();   

    /*void *pInputBuffer = NULL;
    void *pOutputBuffer = NULL;
    ULONG ulInputBufferSize = 0;
    ULONG ulOutputBufferSize = 0;
    ULONG ulStatus = 0 ;
    
    ulOutputBufferSize = 0x100*sizeof(ULONG);
    pOutputBuffer = malloc(ulOutputBufferSize);
    
    //::ExtEscape(hDc,customEscape,sizeof(),(LPCSTR)&structure,sizeof(),(LPSTR)&structure);
    //ULONG ntret = D3DKmtEscape(&esc);
    //Call Escape
    OPREG_Escape esc;

    esc.DoACPIEsc(GFX_ESC_ACPI_SIGNATURE_CODE, 
        ESC_ACPI_READ_MBX,
        GFX_ESCAPE_ACPI_CONTROL,
        &pInputBuffer,
        &pOutputBuffer,
        ulInputBufferSize,
        ulOutputBufferSize,
        &ulStatus);*/

    //ReleaseDC(pdc);
    //OnOK();
}

void CACPI_OP_REGIONDlg::OnTvnSelchangedTreeCtrl(NMHDR *pNMHDR, LRESULT *pResult)
{
    LPNMTREEVIEW pNMTreeView = reinterpret_cast<LPNMTREEVIEW>(pNMHDR);

    // TODO: Add your control notification handler code here
    HTREEITEM hItem = m_MainTreeCtrl.GetSelectedItem();
    DWORD dwData;   
    dwData = m_MainTreeCtrl.GetItemData(hItem);
    dwLastSel = dwData;


    UpdatePage(dwData);    


    *pResult = 0;
}

void CACPI_OP_REGIONDlg::OnBnClickedButtonRefresh()
{
    
    if( ((dwLastSel >= DLG_MBX_ACPI_MAIN) && (dwLastSel <= DLG_MBX_ACPI_MAX)) ||
        ((dwLastSel >= DLG_MBX_BIOS_DRV_MAIN) && (dwLastSel <= DLG_MBX_BIOS_DRV_MAX)))
    {
        if(bFromFile == FALSE)
        {
            bool bACPIMbxValid = m_ACPIMbxMngr.GetMailboxData();   
            UpdatePage(dwLastSel);
        }        
    }
    else if( (dwLastSel >= DLG_ACPI_EVAL_MAIN) && (dwLastSel <= DLG_ACPI_EVAL_MAX))
    {

        switch(dwLastSel)
        {
            case DLG_ACPI_EVAL_DGS:
                cDlgDGSCtrl.Eval(m_ACPIMbxMngr, m_ACPICMMngr);
                break;
            case  DLG_ACPI_EVAL_DOS:
                cDlgDOS.Eval(m_ACPICMMngr);                
                break;
            case DLG_ACPI_EVAL_DOD:
                cDlg_DODCtrl.Eval(m_ACPICMMngr);                
                break;


            case DLG_ACPI_EVAL_DSS:
                
                break;
            case DLG_ACPI_EVAL_DCS:
                //TODO
                break;
            case DLG_ACPI_EVAL_BCL:
                cDlg_BCLCtrl.Update(m_ACPICMMngr);                
                break;
            case DLG_ACPI_EVAL_BQC:
                break;
            case DLG_ACPI_EVAL_BCM:
                cDlg_BCMCtrl.Eval(m_ACPICMMngr);
                break;
 
            default:
                break;
        }

    }
    else if( (dwLastSel >= DLG_EVENTS_MAIN) && (dwLastSel <= DLG_EVENTS_MAX))
    {
        switch(dwLastSel)
        {
            case DLG_EVENTS_LID_CLOSE:
                cDlgLidClose.Update(m_ACPIMbxMngr, m_ACPICMMngr);
                break;
            case DLG_EVENTS_HOTKEY:
                cDlgHkey.Update(m_ACPIMbxMngr, m_ACPICMMngr);
                break;


        }

    }



}

void CACPI_OP_REGIONDlg::UpdatePage(DWORD dwPage)
{
    //Step - 1 Hide all windows
    cDlgASLP.ShowWindow(SW_HIDE);
    cDlgCPDL.ShowWindow(SW_HIDE);
    cDlgCADL.ShowWindow(SW_HIDE);
    cDlgCDCK.ShowWindow(SW_HIDE);
    cDlgCEVT.ShowWindow(SW_HIDE);
    cDlgCHPD.ShowWindow(SW_HIDE);
    cDlgCLID.ShowWindow(SW_HIDE);
    cDlgCDCK.ShowWindow(SW_HIDE);
    cDlgCSTS.ShowWindow(SW_HIDE);
    cDlgDIDL.ShowWindow(SW_HIDE);
    cDlgDRDY.ShowWindow(SW_HIDE);
    cDlgNADL.ShowWindow(SW_HIDE);
    cDlgNRDY.ShowWindow(SW_HIDE);
    cDlgTIDX.ShowWindow(SW_HIDE);

    cDlgARDY.ShowWindow(SW_HIDE);
    cDlgASLC.ShowWindow(SW_HIDE);
    cDlgASLI.ShowWindow(SW_HIDE);
    cDlgBCLP.ShowWindow(SW_HIDE);
    cDlgCBLV.ShowWindow(SW_HIDE);
    cDlgPFIT.ShowWindow(SW_HIDE);
    cDlgTCHE.ShowWindow(SW_HIDE);

    cDlgDGSCtrl.ShowWindow(SW_HIDE);
    cDlgDOS.ShowWindow(SW_HIDE);
    cDlg_BCLCtrl.ShowWindow(SW_HIDE);
    cDlg_BCMCtrl.ShowWindow(SW_HIDE);
    cDlg_DSSCtrl.ShowWindow(SW_HIDE);
    cDlg_DODCtrl.ShowWindow(SW_HIDE);
       
    
    cDlgLidClose.ShowWindow(SW_HIDE);
    cDlgHkey.ShowWindow(SW_HIDE);
    
    

    //Step-2 Handle Cases
    switch(dwPage)
    {
    case DLG_MBX_ACPI_ASLP:        
        cDlgASLP.Update(m_ACPIMbxMngr); 
        cDlgASLP.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CADL:        
        cDlgCADL.Update(m_ACPIMbxMngr); 
        cDlgCADL.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CDCK:
        cDlgCDCK.Update(m_ACPIMbxMngr);
        cDlgCDCK.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CEVT:
        cDlgCEVT.Update(m_ACPIMbxMngr);
        cDlgCEVT.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CHPD:
        cDlgCHPD.Update(m_ACPIMbxMngr);
        cDlgCHPD.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CLID:
        cDlgCLID.Update(m_ACPIMbxMngr);
        cDlgCLID.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CPDL:
        cDlgCPDL.Update(m_ACPIMbxMngr); 
        cDlgCPDL.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_CSTS:
        cDlgCSTS.Update(m_ACPIMbxMngr);
        cDlgCSTS.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_DIDL:
        cDlgDIDL.Update(m_ACPIMbxMngr);
        cDlgDIDL.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_DRDY:
        cDlgDRDY.Update(m_ACPIMbxMngr);
        cDlgDRDY.ShowWindow(SW_SHOW);        
        break;
    case DLG_MBX_ACPI_NADL:
        cDlgNADL.Update(m_ACPIMbxMngr);
        cDlgNADL.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_NRDY:
        cDlgNRDY.Update(m_ACPIMbxMngr);
        cDlgNRDY.ShowWindow(SW_SHOW);
        break;
    case DLG_MBX_ACPI_TIDX:
        cDlgTIDX.Update(m_ACPIMbxMngr);
        cDlgTIDX.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_ARDY:
        cDlgARDY.Update(m_ACPIMbxMngr);
        cDlgARDY.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_BCLP:
        cDlgBCLP.Update(m_ACPIMbxMngr);
        cDlgBCLP.ShowWindow(SW_SHOW);
        break;


    case DLG_MBX_BIOS_DRV_ASLC:
        cDlgASLC.Update(m_ACPIMbxMngr);
        cDlgASLC.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_ASLI:
        
        cDlgASLI.Update(m_ACPIMbxMngr);
        cDlgASLI.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_CBLV:
        cDlgCBLV.Update(m_ACPIMbxMngr);
        cDlgCBLV.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_PFIT:
        cDlgPFIT.Update(m_ACPIMbxMngr);
        cDlgPFIT.ShowWindow(SW_SHOW);
        break;

    case DLG_MBX_BIOS_DRV_TCHE:
        cDlgTCHE.Update(m_ACPIMbxMngr);
        cDlgTCHE.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_DGS:
        cDlgDGSCtrl.Update(m_ACPIMbxMngr, m_ACPICMMngr);
        cDlgDGSCtrl.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_DOS:
        cDlgDOS.Update(m_ACPICMMngr);
        cDlgDOS.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_BCL:
        cDlg_BCLCtrl.Update(m_ACPICMMngr);
        cDlg_BCLCtrl.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_BCM:
        cDlg_BCMCtrl.Update(m_ACPICMMngr);
        cDlg_BCMCtrl.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_DSS:
        cDlg_DSSCtrl.Update(m_ACPICMMngr);
        cDlg_DSSCtrl.ShowWindow(SW_SHOW);
        break;

    case DLG_ACPI_EVAL_DOD:
        cDlg_DODCtrl.Update(m_ACPICMMngr);
        cDlg_DODCtrl.ShowWindow(SW_SHOW);
        break;

    
    //Events
    case DLG_EVENTS_LID_CLOSE:
        cDlgLidClose.Update(m_ACPIMbxMngr,m_ACPICMMngr);
        cDlgLidClose.ShowWindow(SW_SHOW);
        break;

    case DLG_EVENTS_HOTKEY:
        cDlgHkey.Update(m_ACPIMbxMngr,m_ACPICMMngr);
        cDlgHkey.ShowWindow(SW_SHOW);
        break;



    default:
        break;

    }
}
void CACPI_OP_REGIONDlg::OnBnClickedButtonLoad()
{
    char szFile[260];       // buffer for file name
    HWND hwnd = this->m_hWnd;              // owner window
    //    HANDLE hf;              // file handle

    // Initialize OPENFILENAME
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = (LPWSTR)szFile;
    //
    // Set lpstrFile[0] to '\0' so that GetOpenFileName does not 
    // use the contents of szFile to initialize itself.
    //
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"All\0*.*\0Text\0*.TXT\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    // Display the Open dialog box. 
    CFileException fileException;
    CFile myFile;
    if (GetOpenFileName(&ofn) == TRUE) 
    {
        if ( !myFile.Open(ofn.lpstrFile, CFile::modeReadWrite, &fileException ) )
        {
            //Exception
        }
        else
        {
            char buf[100];
            myFile.Read(buf, 10);
            myFile.Close();
        }
    }
}

void CACPI_OP_REGIONDlg::OnLoadFromfile()
{
    // TODO: Add your command handler code here
    //MessageBox(L"test",0,0);
    char szFile[260];       // buffer for file name
    HWND hwnd = this->m_hWnd;              // owner window
    HANDLE hf;              // file handle
    char buffer[500];
    ULONG ulSignature;

    // Initialize OPENFILENAME
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = (LPWSTR)szFile;
    //
    // Set lpstrFile[0] to '\0' so that GetOpenFileName does not 
    // use the contents of szFile to initialize itself.
    //
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"Opregion Dump File(*.DMP)\0*.DMP\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    // Display the Open dialog box. 
    CFileException fileException;
    CFile myFile;
    if (GetOpenFileName(&ofn) == TRUE) 
    {
        if ( !myFile.Open(ofn.lpstrFile, CFile::modeReadWrite, &fileException ) )
        {
            //Exception
        }
        else
        {
            myFile.Read(&ulSignature, 0x4);
            if(ulSignature == 0x8086)

            {
                
                bFromFile = TRUE;
                myFile.Read(buffer, 0x100);
                memcpy(&m_ACPIMbxMngr.stACPIMbx, buffer, 0x100);

                myFile.Read(buffer, 0x100);
                memcpy(&m_ACPIMbxMngr.stBiosDriverMailbox, buffer, 0x100);
            }
            else
            {
                MessageBox(L"Invalid file or file corrupted",0,0);
            }

            myFile.Close();
            UpdatePage(dwLastSel);
        }
    }
}   

void CACPI_OP_REGIONDlg::OnLoadFromsystem()
{
    
    if(NULL != OpenAdapter)
    {
        bFromFile = FALSE;
        bool bACPIMbxValid = m_ACPIMbxMngr.GetMailboxData();   
        UpdatePage(dwLastSel);
    }
    else
    {
        MessageBox(L"Could not retrieve data from Opregion", 0, 0);
    }
}


void CACPI_OP_REGIONDlg::OnFileSave32773()
{
    // TODO: Add your command handler code here
    //MessageBox(L"test",0,0);
    char szFile[260];       // buffer for file name
    HWND hwnd = this->m_hWnd;              // owner window
    HANDLE hf;              // file handle
    DWORD ulBytes = 0;
    ULONG ulSignature = 0x8086;
    //char buffer[500];

    // Initialize OPENFILENAME
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = (LPWSTR)szFile;
    //
    // Set lpstrFile[0] to '\0' so that GetOpenFileName does not 
    // use the contents of szFile to initialize itself.
    //
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"Opregion Dump File(*.DMP)\0*.DMP\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_SHOWHELP | OFN_OVERWRITEPROMPT;

    // Display the Open dialog box. 
    CFileException fileException;
    CFile myFile;
    if (GetSaveFileName(&ofn) == TRUE) 
    {
        hf = CreateFile(ofn.lpstrFile,GENERIC_READ|GENERIC_WRITE, 
            FILE_SHARE_READ,NULL,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,NULL); 

        WriteFile(hf, &ulSignature, 0x4, (LPDWORD)&ulBytes, NULL);
        WriteFile(hf, &m_ACPIMbxMngr.stACPIMbx, 0x100, (LPDWORD)&ulBytes, NULL);
        WriteFile(hf, &m_ACPIMbxMngr.stBiosDriverMailbox, 0x100, (LPDWORD)&ulBytes, NULL);

        if(hf)
        {
            CloseHandle(hf);
        }
      
    }

}
