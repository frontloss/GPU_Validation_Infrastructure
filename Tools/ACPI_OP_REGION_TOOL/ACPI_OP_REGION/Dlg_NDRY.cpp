// Dlg_NDRY.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_NDRY.h"
#include "stdlib.h"


// CDlg_NDRY dialog

IMPLEMENT_DYNAMIC(CDlg_NDRY, CDialog)

CDlg_NDRY::CDlg_NDRY(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_NDRY::IDD, pParent)
{

}

CDlg_NDRY::~CDlg_NDRY()
{
}

void CDlg_NDRY::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulNRDY = 0;
    ulNRDY = m_ACPIMailboxManager.stACPIMbx.ulDriverStatus;

    m_NRDYCombo.ResetContent();

    m_NRDYCombo.AddString(L"Driver not initialized (0)");
    m_NRDYCombo.SetItemData(0,0);

    m_NRDYCombo.AddString(L"3D Application Running (1)");
    m_NRDYCombo.SetItemData(1,1);

    m_NRDYCombo.AddString(L"Overlay Active (2)");
    m_NRDYCombo.SetItemData(2,2);

    m_NRDYCombo.AddString(L"Full Screen DOS Active (3)");
    m_NRDYCombo.SetItemData(3,3);

    m_NRDYCombo.AddString(L"Resource in Use (4)");
    m_NRDYCombo.SetItemData(4,4);

    m_NRDYCombo.AddString(L"Driver in Low power transition (5)");
    m_NRDYCombo.SetItemData(5,5);

    m_NRDYCombo.AddString(L"Extended Desktop Active (6)");
    m_NRDYCombo.SetItemData(6,6);

    m_NRDYCombo.AddString(L"Fatal Failure (7)");
    m_NRDYCombo.SetItemData(7,7);

    m_NRDYCombo.AddString(L"LVDS Power State Change Failed (101)");
    m_NRDYCombo.SetItemData(8,0x101);

    m_NRDYCombo.AddString(L"No Change in Configuration (102)");
    m_NRDYCombo.SetItemData(9,0x102);

    m_NRDYCombo.AddString(L"Get Next Configuration Failed (103)");
    m_NRDYCombo.SetItemData(10,0x103);

    m_NRDYCombo.AddString(L"Get Hotkey List Failed (104)");
    m_NRDYCombo.SetItemData(11,0x104);

    m_NRDYCombo.AddString(L"Turn off all displays rejected (105)");
    m_NRDYCombo.SetItemData(12,0x105);

    m_NRDYCombo.AddString(L"Get Display Info Failed (106)");
    m_NRDYCombo.SetItemData(13,0x106);

    m_NRDYCombo.AddString(L"Invalid ASL Notification (107)");
    m_NRDYCombo.SetItemData(14,0x107);

    m_NRDYCombo.AddString(L"Invalid Buffer Size (108)");
    m_NRDYCombo.SetItemData(15,0x108);

    m_NRDYCombo.AddString(L"EM Not Initialized (109)");
    m_NRDYCombo.SetItemData(16,0x109);

    m_NRDYCombo.AddString(L"TMM Active (10A)");
    m_NRDYCombo.SetItemData(17,0x10A);

    if((ulNRDY >=0 && ulNRDY <= 7) ||
        (ulNRDY >=0x100 && ulNRDY <= 0x10A))
    {
        m_NRDYCombo.SetCurSel(ulNRDY);
    }
    else
    {
        m_NRDYCombo.AddString(L"Invalid Data");
        m_NRDYCombo.SetItemData(18,0x10B);
        m_NRDYCombo.SetCurSel(2);
    }

    UpdateData(FALSE);

}

void CDlg_NDRY::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_NRDY, m_NRDYCombo);
}


BEGIN_MESSAGE_MAP(CDlg_NDRY, CDialog)
END_MESSAGE_MAP()


// CDlg_NDRY message handlers
