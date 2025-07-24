// Dlg_DOS.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_DOS.h"
#include "stdlib.h"



// CDlg_DOS dialog

IMPLEMENT_DYNAMIC(CDlg_DOS, CDialog)

CDlg_DOS::CDlg_DOS(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_DOS::IDD, pParent)
{

}

CDlg_DOS::~CDlg_DOS()
{
}

void CDlg_DOS::Update(ACPIControlMethodManager m_ACPICMMngrMailboxManager)
{
    m_DOS_Switch.ResetContent();
    m_Combo_DOS_AutoDim.ResetContent();


    m_DOS_Switch.AddString(L"Enable Display Switching(0)");
    m_DOS_Switch.SetItemData(0,ACPI_SWITCH_DRIVER_CYCLE_OUTPUT);

    m_DOS_Switch.AddString(L"Disable Display Switching(2)");
    m_DOS_Switch.SetItemData(1,ACPI_SWITCH_DO_NOTHING);

  
    m_Combo_DOS_AutoDim.AddString(L"Enable Auto-Dimming");
    m_Combo_DOS_AutoDim.SetItemData(0,1);

    m_Combo_DOS_AutoDim.AddString(L"Disable Auto-Dimming");
    m_Combo_DOS_AutoDim.SetItemData(1,0);
    
    UpdateData(FALSE);
}

void CDlg_DOS::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_STATIC_DOS1, m_Combo_DOS_DispSW);
    DDX_Control(pDX, IDC_COMBO_DOS2, m_Combo_DOS_AutoDim);
    DDX_Control(pDX, IDC_COMBO_DOS1, m_DOS_Switch);
}


BEGIN_MESSAGE_MAP(CDlg_DOS, CDialog)
    ON_BN_CLICKED(IDC_BUTTON1, &CDlg_DOS::OnBnClickedButton1)
END_MESSAGE_MAP()


// CDlg_DOS message handlers

void CDlg_DOS::OnBnClickedButton1()
{

}

void CDlg_DOS::Eval(ACPIControlMethodManager m_ACPICMMngrMailboxManager)
{
    ACPI_DOS_INPUT stDosIn ;
    ULONG ulAutoDimEnable = 0;

    ZeroMemory(&stDosIn, sizeof(ACPI_DOS_INPUT));
    
    ULONG ulDispSWIndex = m_DOS_Switch.GetCurSel();
    stDosIn.SwitchFlags = (ACPI_SWITCH_FLAGS) m_DOS_Switch.GetItemData(ulDispSWIndex);

    ULONG ulAutoDimIndex = m_Combo_DOS_AutoDim.GetCurSel();
    ulAutoDimEnable = m_Combo_DOS_AutoDim.GetItemData(ulAutoDimIndex);
    if(ulAutoDimEnable)
    {
        stDosIn.bNoAutoDimDC = FALSE;
    }
    else
    {
        stDosIn.bNoAutoDimDC = TRUE;
    }
    
    m_ACPICMMngrMailboxManager.EvaluateControlMethod(
        ESC_ACPI_SET_OUTPUT_SWITCHING,
        sizeof(ACPI_DOS_INPUT),
        0,
        (PVOID) &stDosIn,
        NULL);

}
