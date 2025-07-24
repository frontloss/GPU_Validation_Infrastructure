// Dlg_PFIT.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_PFIT.h"
#include "stdlib.h"


// CDlg_PFIT dialog

IMPLEMENT_DYNAMIC(CDlg_PFIT, CDialog)

CDlg_PFIT::CDlg_PFIT(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_PFIT::IDD, pParent)
{

}

CDlg_PFIT::~CDlg_PFIT()
{
}

void CDlg_PFIT::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCentering = 0, ulTxtModeStretched = 0, ulGfxModeStretched   = 0;
    ULONG ulValid = 0 ;
    ulCentering = m_ACPIMailboxManager.stBiosDriverMailbox.ulPFIT.Centering;
    ulTxtModeStretched = m_ACPIMailboxManager.stBiosDriverMailbox.ulPFIT.TextModeStretch;
    ulGfxModeStretched = m_ACPIMailboxManager.stBiosDriverMailbox.ulPFIT.GfxModeStretch;
    ulValid = m_ACPIMailboxManager.stBiosDriverMailbox.ulPFIT.FieldValidBit;


    m_PFITComboCenter.ResetContent();
    m_PFITComboTxtModeStr.ResetContent();
    m_PFITComboGfxModeStr.ResetContent();


    m_PFITComboCenter.AddString(L"Not requested (0)");
    m_PFITComboCenter.SetItemData(0,0);

    m_PFITComboCenter.AddString(L"Requested (1)");
    m_PFITComboCenter.SetItemData(1,1);

    if((ulCentering >=0 && ulCentering <= 1))
    {
        m_PFITComboCenter.SetCurSel(ulCentering);
    }
    else
    {
        m_PFITComboCenter.AddString(L"Invalid Data");
        m_PFITComboCenter.SetItemData(2,2);
        m_PFITComboCenter.SetCurSel(2);
    }

    m_PFITComboTxtModeStr.AddString(L"Not requested (0)");
    m_PFITComboTxtModeStr.SetItemData(0,0);

    m_PFITComboTxtModeStr.AddString(L"Requested (1)");
    m_PFITComboTxtModeStr.SetItemData(1,1);

    if((ulTxtModeStretched >=0 && ulTxtModeStretched <= 1))
    {
        m_PFITComboTxtModeStr.SetCurSel(ulTxtModeStretched);
    }
    else
    {
        m_PFITComboTxtModeStr.AddString(L"Invalid Data");
        m_PFITComboTxtModeStr.SetItemData(2,2);
        m_PFITComboTxtModeStr.SetCurSel(2);
    }
    UpdateData(FALSE);


    m_PFITComboGfxModeStr.AddString(L"Not requested (0)");
    m_PFITComboGfxModeStr.SetItemData(0,0);

    m_PFITComboGfxModeStr.AddString(L"Requested (1)");
    m_PFITComboGfxModeStr.SetItemData(1,1);

    if((ulGfxModeStretched >=0 && ulGfxModeStretched <= 1))
    {
        m_PFITComboGfxModeStr.SetCurSel(ulGfxModeStretched);
    }
    else
    {
        m_PFITComboGfxModeStr.AddString(L"Invalid Data");
        m_PFITComboGfxModeStr.SetItemData(2,2);
        m_PFITComboGfxModeStr.SetCurSel(2);
    }
    UpdateData(FALSE);

}


void CDlg_PFIT::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_PFIT_CNTR, m_PFITComboCenter);
    DDX_Control(pDX, IDC_COMBO_PFIT_STR, m_PFITComboTxtModeStr);
    DDX_Control(pDX, IDC_COMBO_PFIT_GRMS, m_PFITComboGfxModeStr);
}


BEGIN_MESSAGE_MAP(CDlg_PFIT, CDialog)
END_MESSAGE_MAP()


// CDlg_PFIT message handlers
