// Dlg_SeqHkey.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_SeqHkey.h"
#include "stdlib.h"

// CDlg_SeqHkey dialog

IMPLEMENT_DYNAMIC(CDlg_SeqHkey, CDialog)

CDlg_SeqHkey::CDlg_SeqHkey(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_SeqHkey::IDD, pParent)
{

}

CDlg_SeqHkey::~CDlg_SeqHkey()
{
}

void CDlg_SeqHkey::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_SEQ_HKEY_CTRL, m_SeqHkey);
}

void CDlg_SeqHkey::Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    bool bRet = false;
    static bool uiInit = false;

    //Clear the list control
    m_SeqHkey.DeleteAllItems();


    if(false == uiInit)
    {

        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
        lvColumn.fmt = LVCFMT_LEFT;
        lvColumn.cx = 200;
        lvColumn.pszText = L"Description";
        m_SeqHkey.InsertColumn(0, &lvColumn);

        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
        lvColumn.fmt = LVCFMT_LEFT;
        lvColumn.cx = 80;
        lvColumn.pszText = L"Output";
        m_SeqHkey.InsertColumn(1, &lvColumn);

        uiInit = true;
    }

  
    ACPI_SEQ_HKEY_ARGS stHkeySeq = {0};

    bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_READ_SEQ_HKEY,
         0, sizeof(ACPI_SEQ_HKEY_ARGS), 
        NULL, (PVOID) &stHkeySeq);


    m_SeqHkey.InsertItem(0, L"Notify(VGA,0x80) received");

    switch(stHkeySeq.ulNotifyHkey)
    {
    case 0:
        m_SeqHkey.SetItemText(0, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqHkey.SetItemText(0, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqHkey.SetItemText(0, 1, L"FAILURE");
        break;
    }

    m_SeqHkey.InsertItem(1, L"System BIOS updated Notification as Dispatched");
    switch(stHkeySeq.ulNotificationDispatched)
    {
    case 0:
        m_SeqHkey.SetItemText(1, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqHkey.SetItemText(1, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqHkey.SetItemText(1, 1, L"FAILURE");
        break;
    }

    m_SeqHkey.InsertItem(2, L"Event type updated by System BIOS as ACPI Hotkey");
    switch(stHkeySeq.ulVerifyEventType)
    {
    case 0:
        m_SeqHkey.SetItemText(2, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqHkey.SetItemText(2, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqHkey.SetItemText(2, 1, L"FAILURE");
        break;
    }

    m_SeqHkey.InsertItem(3,L"Event Manger handled event successfully!");

    switch(stHkeySeq.ulEMHandledHkey)
    {
    case 0:
        m_SeqHkey.SetItemText(3, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqHkey.SetItemText(3, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqHkey.SetItemText(3, 1, L"FAILURE");
        break;
    }

    m_SeqHkey.InsertItem(4, L"Success/failure indicated by driver");
    switch(stHkeySeq.ulNotificationUpdated)
    {
    case 0:
        m_SeqHkey.SetItemText(4, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqHkey.SetItemText(4, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqHkey.SetItemText(4, 1, L"FAILURE");
        break;
    }
  

    UpdateData(FALSE);
}



BEGIN_MESSAGE_MAP(CDlg_SeqHkey, CDialog)
END_MESSAGE_MAP()


// CDlg_SeqHkey message handlers
