// Seq_Lid.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Seq_Lid.h"
#include "stdlib.h"

// CSeq_Lid dialog

IMPLEMENT_DYNAMIC(CSeq_Lid, CDialog)

CSeq_Lid::CSeq_Lid(CWnd* pParent /*=NULL*/)
	: CDialog(CSeq_Lid::IDD, pParent)
{

}

CSeq_Lid::~CSeq_Lid()
{
}

void CSeq_Lid::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_LIST1, m_SeqLidClose);
}

void CSeq_Lid::Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    bool bRet = false;
    static bool uiInit = false;

    //Clear the list control
    m_SeqLidClose.DeleteAllItems();


    if(false == uiInit)
    {

        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
        lvColumn.fmt = LVCFMT_LEFT;
        lvColumn.cx = 200;
        lvColumn.pszText = L"Description";
        m_SeqLidClose.InsertColumn(0, &lvColumn);

        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
        lvColumn.fmt = LVCFMT_LEFT;
        lvColumn.cx = 80;
        lvColumn.pszText = L"Output";
        m_SeqLidClose.InsertColumn(1, &lvColumn);

        uiInit = true;
    }

  
    ACPI_SEQ_LID_ARGS stLidSeq = {0};

    //Evaluate _DGS for each Child Device
    bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_READ_SEQ_LID,
         0, sizeof(ACPI_SEQ_LID_ARGS), 
        NULL, (PVOID) &stLidSeq);


    m_SeqLidClose.InsertItem(0, L"Notify(LID,0x80) received");

    switch(stLidSeq.ulNotifyLid)
    {
    case 0:
        m_SeqLidClose.SetItemText(0, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(0, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(0, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(1, L"Adapter is ready to handle ACPI notifications");
    switch(stLidSeq.ulAdapterReady)
    {
    case 0:
        m_SeqLidClose.SetItemText(1, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(1, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(1, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(2, L"Lid status updated in ACPI OpRegion");
    switch(stLidSeq.ulDriverLidStatus)
    {
    case 0:
        m_SeqLidClose.SetItemText(2, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(2, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(2, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(3,L"Event Manger handled lid successfully!");

    switch(stLidSeq.ulEMHandledEvent)
    {
    case 0:
        m_SeqLidClose.SetItemText(3, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(3, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(3, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(4, L"ACPI OpRegion updated with lid notification handling status");
    switch(stLidSeq.ulNotificationUpdated)
    {
    case 0:
        m_SeqLidClose.SetItemText(4, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(4, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(4, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(5, L"OS notified about lid status change");
    switch(stLidSeq.ulOSInformedAboutLid )
    {
    case 0:
        m_SeqLidClose.SetItemText(5, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(5, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(5, 1, L"FAILURE");
        break;
    }

    m_SeqLidClose.InsertItem(6, L"Panel power changed successfully!");
    switch(stLidSeq.ulPanelPowerChanged  )
    {
    case 0:
        m_SeqLidClose.SetItemText(6, 1, L"NOT DONE");
        break;
    case 1:
        m_SeqLidClose.SetItemText(6, 1, L"SUCCESS");
        break;
    case 2:
        m_SeqLidClose.SetItemText(6, 1, L"FAILURE");
        break;
    }

    UpdateData(FALSE);
}


BEGIN_MESSAGE_MAP(CSeq_Lid, CDialog)
END_MESSAGE_MAP()


// CSeq_Lid message handlers
