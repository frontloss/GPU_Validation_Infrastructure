// Dlg_ASLC.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_ASLC.h"
#include "stdlib.h"


// CDlg_ASLC dialog

IMPLEMENT_DYNAMIC(CDlg_ASLC, CDialog)

CDlg_ASLC::CDlg_ASLC(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_ASLC::IDD, pParent)
{

}

CDlg_ASLC::~CDlg_ASLC()
{
}

void CDlg_ASLC::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_ALSC_ALS, m_ASLCComboALS);
    DDX_Control(pDX, IDC_COMBO_ALSC_BLC, m_ASLCComboBKT);
    DDX_Control(pDX, IDC_COMBO_ALSC_PFIT, m_ASLCComboPFIT);
}

void CDlg_ASLC::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulALS = 0, ulBKT = 0, ulPFIT = 0;
    ulALS = m_ACPIMailboxManager.stBiosDriverMailbox.ulASLEIntCommand.ALSEvent;
    ulBKT = m_ACPIMailboxManager.stBiosDriverMailbox.ulASLEIntCommand.BLCEvent;
    ulPFIT = m_ACPIMailboxManager.stBiosDriverMailbox.ulASLEIntCommand.PFITEvent;

    m_ASLCComboALS.ResetContent();
    m_ASLCComboBKT.ResetContent();
    m_ASLCComboPFIT.ResetContent();


    m_ASLCComboALS.AddString(L"No request or already serviced (0)");
    m_ASLCComboALS.SetItemData(0,0);

    m_ASLCComboALS.AddString(L"Service Requested (1)");
    m_ASLCComboALS.SetItemData(1,1);

    if((ulALS >=0 && ulALS <= 1))
    {
        m_ASLCComboALS.SetCurSel(ulALS);
    }
    else
    {
        m_ASLCComboALS.AddString(L"Invalid Data");
        m_ASLCComboALS.SetItemData(2,2);
        m_ASLCComboALS.SetCurSel(2);
    }

    m_ASLCComboBKT.AddString(L"No request or already serviced (0)");
    m_ASLCComboBKT.SetItemData(0,0);

    m_ASLCComboBKT.AddString(L"Service Requested (1)");
    m_ASLCComboBKT.SetItemData(1,1);

    if((ulBKT >=0 && ulBKT <= 1))
    {
        m_ASLCComboBKT.SetCurSel(ulALS);
    }
    else
    {
        m_ASLCComboBKT.AddString(L"Invalid Data");
        m_ASLCComboBKT.SetItemData(2,2);
        m_ASLCComboBKT.SetCurSel(2);
    }

    m_ASLCComboPFIT.AddString(L"No request or already serviced (0)");
    m_ASLCComboPFIT.SetItemData(0,0);

    m_ASLCComboPFIT.AddString(L"Service Requested (1)");
    m_ASLCComboPFIT.SetItemData(1,1);

    if((ulPFIT >=0 && ulPFIT <= 1))
    {
        m_ASLCComboPFIT.SetCurSel(ulALS);
    }
    else
    {
        m_ASLCComboPFIT.AddString(L"Invalid Data");
        m_ASLCComboPFIT.SetItemData(2,2);
        m_ASLCComboPFIT.SetCurSel(2);
    }

    UpdateData(FALSE);

}


BEGIN_MESSAGE_MAP(CDlg_ASLC, CDialog)
    ON_STN_CLICKED(IDC_STATIC_DRDY1, &CDlg_ASLC::OnStnClickedStaticDrdy1)
END_MESSAGE_MAP()


// CDlg_ASLC message handlers

void CDlg_ASLC::OnStnClickedStaticDrdy1()
{
    // TODO: Add your control notification handler code here
}
