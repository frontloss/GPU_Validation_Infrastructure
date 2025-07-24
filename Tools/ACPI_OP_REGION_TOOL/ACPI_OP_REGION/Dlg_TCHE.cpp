// Dlg_TCHE.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_TCHE.h"
#include "stdlib.h"


// CDlg_TCHE dialog

IMPLEMENT_DYNAMIC(CDlg_TCHE, CDialog)

CDlg_TCHE::CDlg_TCHE(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_TCHE::IDD, pParent)
{

}

CDlg_TCHE::~CDlg_TCHE()
{
}

void CDlg_TCHE::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulALS = 0, ulBKT = 0, ulPFIT = 0;
    ulALS = m_ACPIMailboxManager.stBiosDriverMailbox.ulTCHE.ALSEvent;
    ulBKT = m_ACPIMailboxManager.stBiosDriverMailbox.ulTCHE.BLCEvent;
    ulPFIT = m_ACPIMailboxManager.stBiosDriverMailbox.ulTCHE.PFITEvent;

    m_ASLCComboALS.ResetContent();
    m_ASLCComboBKT.ResetContent();
    m_ASLCComboPFIT.ResetContent();


    m_ASLCComboALS.AddString(L"Disabled (0)");
    m_ASLCComboALS.SetItemData(0,0);

    m_ASLCComboALS.AddString(L"Enabled (1)");
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

    m_ASLCComboBKT.AddString(L"Disabled (0)");
    m_ASLCComboBKT.SetItemData(0,0);

    m_ASLCComboBKT.AddString(L"Enabled (1)");
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

    m_ASLCComboPFIT.AddString(L"Disabled (0)");
    m_ASLCComboPFIT.SetItemData(0,0);

    m_ASLCComboPFIT.AddString(L"Enabled (1)");
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


void CDlg_TCHE::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_ALS, m_ASLCComboALS);
    DDX_Control(pDX, IDC_COMBO_BLC, m_ASLCComboBKT);
    DDX_Control(pDX, IDC_COMBO_PFIT, m_ASLCComboPFIT);
}


BEGIN_MESSAGE_MAP(CDlg_TCHE, CDialog)
END_MESSAGE_MAP()


// CDlg_TCHE message handlers
